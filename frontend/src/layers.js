import {Subject} from 'rxjs/Subject'
import L from 'leaflet'

import {maxProp, PARTY_COLORS, asyncChunks} from './helpers'

class BaseLayer {
  constructor () {
    this.config = {}
    this._cb = function () {}
    this.config.defaultStyle = this.config.defaultStyle || {
      style: styleDistrict
    }
    this.config.emphazisedStyle = this.config.emphazisedStyle || {
      style () { return {color: '#0078FF', weight: 1, opacity: 0.7} }
    }
    this.layers = L.layerGroup([])
  }

  selectDistrict (layer) {
    if (this._selectedLayer === layer) {
      this.reset()
      this._cb(undefined)
      return
    }
    this.reset()
    this._selectedLayer = layer
    layer.setStyle(this.config.emphazisedStyle.style(layer.feature))
    this._cb(layer.feature)
  }

  reset () {
    if (this._selectedLayer) {
      this._selectedLayer.setStyle(this.config.defaultStyle.style(this._selectedLayer.feature))
    }
    this._selectedLayer = undefined
  }

  onSelection (cb) {
    this._cb = cb
  }
}

export class DistrictLayer extends BaseLayer {
  updateDistricts (districts) {
    if (!districts) {
      return
    }
    const chunks = []
    for (let i = 0; i < districts.length; i += 50) {
      chunks.push(districts.slice(i, i + 50))
    }
    const $this = this
    this.layers.clearLayers()
    asyncChunks(districts, 400, 50).subscribe((district) => {
      const layer = L.geoJSON(district, this.config.defaultStyle)
      layer.on('click', function ({layer}) {
        $this.selectDistrict.bind($this)(layer)
      })
      this.layers.addLayer(layer)
    })
  }
}

export class CountyLayer extends BaseLayer {
  constructor (clickable) {
    super()
    this._countyLayers = {}
    this.clickable = Boolean(clickable)
  }

  updateCounty (county) {
    if (!county) {
      return
    }
    const bwk = county.properties.bwk
    if (this._countyLayers[bwk]) {
      this.layers.removeLayer(this._countyLayers[bwk])
    }
    const $this = this
    const layer = L.geoJSON(county, this.config.defaultStyle)
    if (this.clickable) {
      layer.on('click', function ({layer}) {
        $this.selectDistrict.bind($this)(layer)
      })
    }
    this.layers.addLayer(layer)
    this._countyLayers[bwk] = layer
  }
}

export class AnimationLayer {
  constructor (districts, counties) {
    this.layers = L.layerGroup([])
    this.districts = districts
    this.counties = counties
    this.grow = new CountyLayer(false)
    this.gSteps = []
    this._status = new Subject()
  }

  get status () {
    return this._status.asObservable()
  }

  downloadSteps () {
    fetch('/api/gsteps').then(resp => {
      if (resp.status !== 200) {
        throw new Error('gsteps returned a 404 error code')
      }
      return resp.json()
    }).then(gsteps => {
      this.gSteps = gsteps
      if (this.gSteps[this.gSteps.length - 1].action !== 'stop') {
        window.setTimeout(this.downloadSteps.bind(this), 1000)
      }
    })
  }

  run () {
    this.downloadSteps()
    let gIndex = -1

    const interating = window.setInterval(() => {
      if (gIndex < this.gSteps.length - 2) {
        gIndex = gIndex + 1
        this.nextStep(gIndex)
      }
      if (gIndex > -1 && this.gSteps[gIndex].action === 'stop') {
        window.clearInterval(interating)
      }
    }, 500)
  }

  nextStep (index) {
    const gStep = this.gSteps[index]
    this._status.next(gStep.action)
    if (gStep.action === 'search') {
      this.onSearch(gStep)
      return
    }
    if (this.gSteps[index - 1].action === 'search' && gStep.action === 'grow') {
      this.layers.clearLayers()
      this.layers.addLayer(this.grow.layers)
      Object.keys(this.counties).map(key => this.counties[key]).forEach(county => {
        this.grow.updateCounty(county)
      })
    }
    if (gStep.action === 'grow' || gStep.action === 'cleanup') {
      gStep.targets.forEach(county => this.grow.updateCounty(county))
    }
  }

  onSearch ({candidates, winner}) {
    this.layers.clearLayers()
    for (let candidate of candidates) {
      let shape = this.districts[candidate]
      const fillColor = candidate === winner ? 'green' : 'yellow'
      let layer = L.geoJSON(shape, {color: 'black', fillColor, weight: 1, fillOpacity: 0.5})
      this.layers.addLayer(layer)
    }
  }
}

function styleDistrict ({geometry}) {
  const {properties} = geometry
  const winner = maxProp(properties.result)
  return {color: PARTY_COLORS[winner], weight: 1, opacity: 0.65}
}

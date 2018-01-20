import L from 'leaflet'
import {Observable} from 'rxjs/Observable'
import 'rxjs/add/observable/empty'
import 'rxjs/add/observable/of'
import 'rxjs/add/observable/timer'
import 'rxjs/add/operator/concat'
import 'rxjs/add/operator/mapTo'

import {maxProp, PARTY_COLORS} from './helpers'

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
    const schedule = chunks.map(function (chunk, index) {
      if (index === 0) {
        return Observable.of(chunk)
      }
      return Observable.timer(300).mapTo(chunk)
    }).reduce(function (obs, val) {
      return obs.concat(val)
    }, Observable.empty())
    schedule.subscribe(function (chunk) {
      chunk.forEach(function (district) {
        const layer = L.geoJSON(district, this.config.defaultStyle)
        layer.on('click', function ({layer}) {
          $this.selectDistrict.bind($this)(layer)
        })
        this.layers.addLayer(layer)
      }.bind($this))
    })
  }
}

export class CountyLayer extends BaseLayer {
  constructor () {
    super()
    this._countyLayers = {}
  }

  updateCounty (county) {
    if (!county) {
      return
    }
    const bwk = county.properties.bwk
    if (this._countyLayers[bwk]) {
      this._countyLayers[bwk].remove()
    }
    const $this = this
    const layer = L.geoJSON(county, this.config.defaultStyle)
    layer.on('click', function ({layer}) {
      $this.selectDistrict.bind($this)(layer)
    })
    this.layers.addLayer(layer)
    this._countyLayers[bwk] = layer
  }
}

function styleDistrict ({geometry}) {
  const {properties} = geometry
  const winner = maxProp(properties.result)
  return {color: PARTY_COLORS[winner], weight: 1, opacity: 0.65}
}

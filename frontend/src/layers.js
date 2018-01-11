import L from 'leaflet'

import {maxProp, PARTY_COLORS} from './helpers'

export class DistrictLayer {
  constructor (config, editable = false) {
    this.config = config || {}
    this._cb = function () {}
    this.config.defaultStyle = this.config.defaultStyle || {
      style: styleDistrict
    }
    this.config.emphazisedStyle = this.config.emphazisedStyle || {
      style () { return {color: '#0078FF', weight: 1, opacity: 0.7} }
    }
  }

  setDistricts (districts$) {
    this.layers = L.layerGroup([])
    const $this = this
    this.subscription = districts$.subscribe(districts => {
      districts.forEach(function (district) {
        const layer = L.geoJSON(district, this.config.defaultStyle)
        layer.on('click', function ({layer}) {
          $this.selectDistrict.bind($this)(layer)
        })
        this.layers.addLayer(layer)
      }.bind(this))
    })
  }

  selectDistrict (layer) {
    if (this._selectedLayer === layer) {
      this.reset()
      this._cb(undefined)
      return
    }
    // uncomment the line below to make polygon editable.
    // Warning: Performance issues, freezing > 20 secs even on fast CPU systems
    // layer.pm.enable({draggable: false, allowSelfIntersection: false})

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

function styleDistrict ({geometry}) {
  const {properties} = geometry
  const winner = maxProp(properties.result)
  return {color: PARTY_COLORS[winner], weight: 1, opacity: 0.65}
}
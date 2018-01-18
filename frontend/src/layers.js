import L from 'leaflet'

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
    const $this = this
    this.layers.clearLayers()
    districts.forEach(function (district) {
      const layer = L.geoJSON(district, this.config.defaultStyle)
      layer.on('click', function ({layer}) {
        $this.selectDistrict.bind($this)(layer)
      })
      this.layers.addLayer(layer)
    }.bind(this))
  }
}

function styleDistrict ({geometry}) {
  const {properties} = geometry
  const winner = maxProp(properties.result)
  return {color: PARTY_COLORS[winner], weight: 1, opacity: 0.65}
}

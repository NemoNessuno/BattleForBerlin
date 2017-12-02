import L from 'leaflet'

export class DistrictLayer {
  constructor (districts, config) {
    this.config = config || {}
    this.config.defaultStyle = this.config.defaultStyle || {
      style () { return {color: '#FF7800', weight: 1, opacity: 0.65} }
    }
    this.config.emphazisedStyle = this.config.emphazisedStyle || {
      style () { return {color: '#0078FF', weight: 1, opacity: 0.7} }
    }
    this.layers = L.layerGroup(Array(districts).map(function (district, idx) {
      const $this = this
      if (idx === 1) {
        console.log(district)
      }
      const layer = L.geoJSON(district, this.config.defaultStyle)
      layer.on('click', function ({layer}) {
        $this.selectDistrict.bind($this)(layer)
      })
      return layer
    }.bind(this)))
  }

  selectDistrict (layer) {
    if (this._selectedLayer === layer) {
      this.reset()
      return
    }
    this.reset()
    this._selectedLayer = layer
    layer.setStyle(this.config.emphazisedStyle.style())
  }

  reset () {
    if (this._selectedLayer) {
      this._selectedLayer.setStyle(this.config.defaultStyle.style())
    }
    this._selectedLayer = undefined
  }
}

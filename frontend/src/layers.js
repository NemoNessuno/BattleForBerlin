import L from 'leaflet'

const PARTY_COLORS = {
  afd: '#2B9FDB',
  gruene: '#4E8935',
  spd: '#DB0E2A',
  cdu: '#000000',
  fdp: '#FEE943',
  die_linke: '#D8101F'
}

export class DistrictLayer {
  constructor (districts, config) {
    this.config = config || {}
    this.config.defaultStyle = this.config.defaultStyle || {
      style: styleDistrict
    }
    this.config.emphazisedStyle = this.config.emphazisedStyle || {
      style () { return {color: '#0078FF', weight: 1, opacity: 0.7} }
    }
    this.layers = L.layerGroup(Array(districts).map(function (district) {
      const $this = this
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
    layer.setStyle(this.config.emphazisedStyle.style(layer.feature))
  }

  reset () {
    if (this._selectedLayer) {
      this._selectedLayer.setStyle(this.config.defaultStyle.style(this._selectedLayer.feature))
    }
    this._selectedLayer = undefined
  }
}

function styleDistrict ({geometry}) {
  const {properties} = geometry
  let partyMax = ''
  let resultMax = 0
  Object.keys(properties.result).forEach(function (party) {
    if (properties.result[party] > resultMax) {
      partyMax = party
      resultMax = properties.result[party]
    }
  })
  return {color: PARTY_COLORS[partyMax], weight: 1, opacity: 0.65}
}

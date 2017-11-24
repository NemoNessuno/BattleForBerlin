<template>
  <div id="map" name="slide-in">
    <urnenwahlbezirk
      v-if="selectedDistrict > -1"
      :uwb-id="selectedDistrict"
      @close="unselectDistrict" />
  </div>
</template>

<script>
  import L from 'leaflet'
  import Urnenwahlbezirk from './Urnenwahlbezirk'
  const tileLayerAPI = 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}'
  const accessToken = 'pk.eyJ1IjoibmVtb25lc3N1bm8iLCJhIjoiY2phM3FvbGRkM2x6MTM0cGN1M3h6dHcyYiJ9.Gie5hDNbis60D17BFvH31Q'
  const DEFAULT_STYLE = {color: '#FF7800', weight: 1, opacity: 0.65}
  const EMPHAZISED_STYLE = {color: '#0078FF', weight: 1, opacity: 0.7}
  export default {
    name: 'leaflet-map',
    props: {
      uwb: {type: Array, required: true}
    },
    data () {
      return {
        map: undefined,
        uwbLayer: undefined,
        sidebar: undefined,
        selectedLayer: undefined,
        selectedDistrict: -1
      }
    },
    mounted () {
      const tileLayer = L.tileLayer(tileLayerAPI, {
        attribution: `Map data &copy;
        <a href="http://openstreetmap.org">
          OpenStreetMap
        </a>
        contributors,
        <a href="http://creativecommons.org/licenses/by-sa/2.0/">
          CC-BY-SA
        </a>, Imagery ©
        <a href="http://mapbox.com">Mapbox</a>`,
        maxZoom: 18,
        id: 'mapbox.streets',
        accessToken
      })
      this.map = L.map('map', {
        center: [52.5200, 13.4050],
        zoom: 10,
        maxzoom: 13,
        layers: [tileLayer]
      })
      this.$nextTick(function () {
        this.updateUWB(this.uwb)
        L.control.layers({'Urnenwahlbezirke': this.uwbLayer}).addTo(this.map)
      }.bind(this))
    },
    methods: {
      updateUWB (urnenWahlbezirke) {
        const $this = this
        if (this.uwbLayer) {
          this.uwbLayer.remove()
        }
        this.uwbLayer = L.layerGroup(urnenWahlbezirke.map((wahlbezirk, idx) => {
          const layer = L.geoJSON(wahlbezirk, DEFAULT_STYLE)
          layer.on('click', function ({layer}) {
            $this.unselectLayer()
            $this.selectedLayer = layer
            layer.setStyle(EMPHAZISED_STYLE)
            $this.selectedDistrict = idx
          })
          return layer
        }))
        this.uwbLayer.addTo(this.map)
      },
      unselectLayer () {
        if (this.selectedLayer) {
          this.selectedLayer.setStyle(DEFAULT_STYLE)
        }
        this.selectedLayer = undefined
      },
      unselectDistrict () {
        this.unselectLayer()
        this.selectedDistrict = -1
      }
    },
    watch: {
      uwb (newVal, oldVal) {
        this.updateUWB(newVal)
      }
    },
    components: {Urnenwahlbezirk}
  }
</script>

<style>
#map {
  height: calc(100vh - 10em);
  margin: 0.3em;
  border-radius: 5pt;
}
</style>
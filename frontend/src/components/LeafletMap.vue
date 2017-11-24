<template>
  <div id="map" name="slide-in">
    <urnenwahlbezirk v-if="selectedDistrict > -1" :uwb-id="selectedDistrict" @close="selectedDistrict = -1" />
  </div>
</template>

<script>
  import L from 'leaflet'
  import Urnenwahlbezirk from './Urnenwahlbezirk'
  const tileLayerAPI = 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}'
  const accessToken = 'pk.eyJ1IjoibmVtb25lc3N1bm8iLCJhIjoiY2phM3FvbGRkM2x6MTM0cGN1M3h6dHcyYiJ9.Gie5hDNbis60D17BFvH31Q'
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
          const layer = L.geoJSON(wahlbezirk, {color: '#FF7800', weight: 1, opacity: 0.65})
          layer.on('click', function () {
            $this.selectedDistrict = idx
          })
          return layer
        }))
        this.uwbLayer.addTo(this.map)
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
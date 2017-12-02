<template>
  <div id="map" name="slide-in">
  </div>
</template>

<script>
  import L from 'leaflet'
  import DistrictDetails from './DistrictDetails'
  import {DistrictLayer} from '@/layers'
  const tileLayerAPI = 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}'
  const accessToken = 'pk.eyJ1IjoibmVtb25lc3N1bm8iLCJhIjoiY2phM3FvbGRkM2x6MTM0cGN1M3h6dHcyYiJ9.Gie5hDNbis60D17BFvH31Q'
  export default {
    name: 'leaflet-map',
    props: {
      districts: {type: Object, required: true}
    },
    data () {
      return {
        map: undefined,
        ballotLayer: undefined,
        letterLayer: undefined,
        controls: undefined
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
      this.updateLayers()
    },
    methods: {
      updateLayers () {
        const {ballot, letters} = this.districts
        this.ballotLayer = new DistrictLayer(ballot)
        this.letterLayer = new DistrictLayer(letters)
        if (this.controls) {
          this.controls.remove()
        }
        this.ballotLayer.layers.addTo(this.map)
        this.controls = L.control.layers({
          'Urnenwahlbezirke': this.ballotLayer.layers,
          'Briefwahlbezirke': this.letterLayer.layers
        }, {}, {collapsed: false}).addTo(this.map)
      }
    },
    watch: {
      districts (newVal, oldVal) {
        this.updateLayers()
      }
    },
    components: {DistrictDetails}
  }
</script>

<style>
#map {
  height: calc(100vh - 10em);
  margin: 0.3em;
  border-radius: 5pt;
}
</style>

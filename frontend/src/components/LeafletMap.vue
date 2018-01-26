<template>
  <div id="map" name="slide-in" ref="map">
    <district-details
      v-if="currentDistrict"
      @close="unselectItem" />
    <county-details
      v-if="currentCounty"
      @close="unselectItem" />
  </div>
</template>

<script>
  import L from 'leaflet'
  import DistrictDetails from './DistrictDetails'
  import CountyDetails from './CountyDetails'
  import {DistrictLayer, CountyLayer} from '@/layers'
  import {COUNTY_KEYS} from '@/store/constants'
  import {mapState, mapMutations, mapGetters} from 'vuex'
  const tileLayerAPI = 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}'
  const accessToken = 'pk.eyJ1IjoibmVtb25lc3N1bm8iLCJhIjoiY2phM3FvbGRkM2x6MTM0cGN1M3h6dHcyYiJ9.Gie5hDNbis60D17BFvH31Q'
  export default {
    name: 'leaflet-map',
    data () {
      return {
        map: undefined,
        controls: undefined,
        districtLayer: new DistrictLayer(),
        countyWrapper: new CountyLayer()
      }
    },
    computed: {
      ...mapState(['districts', 'gerrymanderAnimation'].concat(COUNTY_KEYS)),
      ...mapGetters(['currentDistrict', 'currentCounty'])
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
        doubleClickZoom: false,
        zoomControl: false,
        layers: [tileLayer]
      })
      this.districtLayer.updateDistricts(this.districts)
      this.districtLayer.onSelection(function (values) {
        if (!values) {
          this.unselectItem()
        } else {
          this.selectDistrict(values.geometry.properties.identifier)
        }
      }.bind(this))
      this.countyLayer = new CountyLayer()
      for (let key of COUNTY_KEYS) {
        this.countyLayer.updateCounty(this[key])
      }
      this.countyLayer.onSelection(function (values) {
        if (!values) {
          this.unselectItem()
        } else {
          this.selectCounty(values.geometry.properties.bwk)
        }
      }.bind(this))
      this.controls = L.control.layers(this.map)
      this.controls = L.control.layers({
        'Wahlbezirke': this.districtLayer.layers,
        'Wahlkreise': this.countyLayer.layers
      }, {}, {collapsed: false}).addTo(this.map)
      this.countyLayer.layers.addTo(this.map)
      for (let key of COUNTY_KEYS) {
        this.$watch(key, function (newVal) {
          this.countyLayer.updateCounty(newVal)
        })
      }
    },
    methods: mapMutations(['selectDistrict', 'selectCounty', 'unselectItem']),
    watch: {
      districts (newVal) {
        this.districtLayer.updateDistricts(newVal)
      }
    },
    components: {DistrictDetails, CountyDetails}
  }
</script>

<style lang="sass">
#map
  margin: 0.3em
  border-radius: 5pt
  height: calc(100vh - 71px)
</style>

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
  import {DistrictLayer} from '@/layers'
  import {mapState, mapMutations, mapGetters} from 'vuex'
  const tileLayerAPI = 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}'
  const accessToken = 'pk.eyJ1IjoibmVtb25lc3N1bm8iLCJhIjoiY2phM3FvbGRkM2x6MTM0cGN1M3h6dHcyYiJ9.Gie5hDNbis60D17BFvH31Q'
  export default {
    name: 'leaflet-map',
    data () {
      return {
        map: undefined,
        controls: undefined,
        mergedWrapper: undefined,
        countyWrapper: undefined
      }
    },
    computed: {
      ...mapState(['districts', 'counties']),
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
        layers: [tileLayer]
      })
      this.mergedWrapper = new DistrictLayer()
      this.mergedWrapper.updateDistricts(this.districts)
      this.mergedWrapper.onSelection(function (values) {
        if (!values) {
          this.unselectItem()
        } else {
          this.selectDistrict(values.geometry.properties.identifier)
        }
      }.bind(this))
      this.countyWrapper = new DistrictLayer()
      this.countyWrapper.updateDistricts(this.counties)
      this.countyWrapper.onSelection(function (values) {
        if (!values) {
          this.unselectItem()
        } else {
          this.selectCounty(values.geometry.properties.bwk)
        }
      }.bind(this))
      this.controls = L.control.layers(this.map)
      this.controls = L.control.layers({
        'Wahlbezirke': this.mergedWrapper.layers,
        'Wahlkreise': this.countyWrapper.layers
      }, {}, {collapsed: false}).addTo(this.map)
      this.mergedWrapper.layers.addTo(this.map)
      this.$nextTick(() => {
        this.$refs.map.nativeElement.addEventListener('transitionend', () => {
          this.map.invalidateSize()
        })
      })
    },
    methods: mapMutations(['selectDistrict', 'selectCounty', 'unselectItem']),
    watch: {
      districts (newVal) {
        this.mergedWrapper.updateDistricts(newVal)
      },
      counties (newVal) {
        this.countyWrapper.updateDistricts(newVal)
      }
    },
    components: {DistrictDetails, CountyDetails}
  }
</script>

<style>
#map {
  margin: 0.3em;
  border-radius: 5pt;
}
</style>

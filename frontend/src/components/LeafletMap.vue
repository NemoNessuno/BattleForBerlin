<template>
  <div id="map" name="slide-in" ref="map">
    <district-details
      v-if="showDistrictDetails" />
    <county-details
      v-if="showCountyDetails" />
  </div>
</template>

<script>
  import L from 'leaflet'
  import DistrictDetails from './DistrictDetails'
  import CountyDetails from './CountyDetails'
  import {DistrictLayer, CountyLayer} from '@/layers'
  import {COUNTY_KEYS} from '@/store/constants'
  import {mapState, mapMutations, mapGetters} from 'vuex'
  import {buildLeafletMap} from '../helpers'
  export default {
    name: 'leaflet-map',
    data () {
      return {
        map: undefined,
        controls: undefined,
        districtLayer: new DistrictLayer(),
        countyLayer: new CountyLayer(true)
      }
    },
    computed: {
      ...mapState(['districts', 'countyProps', 'districtProps'].concat(COUNTY_KEYS)),
      ...mapGetters(['currentDistrict']),
      showCountyDetails () {
        return this.countyProps &&
          this.$route.params.identifier &&
          this.$route.params.identifier.length === 3
      },
      showDistrictDetails () {
        return this.districtProps &&
          this.$route.params.identifier &&
          this.$route.params.identifier.length === 4
      }
    },
    mounted () {
      this.map = buildLeafletMap(this.$el)
      this.districtLayer.updateDistricts(this.districts)
      this.districtLayer.onSelection(function (values) {
        if (!values) {
          this.$router.push('/map')
        } else {
          this.$router.push('/map/' + values.geometry.properties.identifier)
        }
      }.bind(this))
      for (let key of COUNTY_KEYS) {
        this.countyLayer.updateCounty(this[key])
      }
      this.countyLayer.onSelection(function (values) {
        if (!values) {
          this.$router.push('/map')
        } else {
          this.$router.push('/map/' + values.geometry.properties.bwk)
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

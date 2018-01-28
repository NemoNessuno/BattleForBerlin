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
  import {buildLeafletMap} from '../helpers'
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
      ...mapState(['districts', 'gerrymanderAnimation', 'countyProps'].concat(COUNTY_KEYS)),
      ...mapGetters(['currentDistrict']),
      currentCounty () {
        if (this.countyProps && this.$route.params.identifier && this.$route.params.identifier.length === 3) {
          console.log(this.countyProps[this.$route.params.identifier])
          return this.countyProps[this.$route.params.identifier]
        }
        return undefined
      }
    },
    mounted () {
      console.log('MOUNTED')
      this.map = buildLeafletMap(this.$el)
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
      },
      '$route' (to, from) {
        console.log(to)
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

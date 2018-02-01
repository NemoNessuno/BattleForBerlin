<template>
  <div id="map2" />
</template>
<script>
  import {buildLeafletMap} from '../helpers'
  import {COUNTY_KEYS} from '@/store/constants'
  import {SearchLayer, CountyLayer} from '../layers'
  import {mapState, mapGetters} from 'vuex'
  export default {
    name: 'animation-map',
    data () {
      return {
        animationIndex: 0,
        searchRender: undefined,
        growRenderer: undefined
      }
    },
    created () {
      if (!this.gActive) {
        this.$router.push('/map')
      }
    },
    computed: {
      ...mapState(['gActive', 'districtHash'].concat(COUNTY_KEYS)),
      ...mapGetters(['currentGStep']),
      stop () {
        if (!this.gsteps || this.gsteps.length > this.animationIndex + 1) {
          return false
        }
        return this.animationIndex + 1 === this.gstep
      }
    },
    mounted () {
      this.map = buildLeafletMap(this.$el)
      this.searchRenderer = new SearchLayer(this.districtHash)
      this.searchRenderer.layers.addTo(this.map)
      for (let key of COUNTY_KEYS) {
        this.$watch(key, function (newVal) {
          if (this.growRenderer) {
            this.growRenderer.updateCounty(newVal)
          }
        })
      }
      this.$store.dispatch('runAnimation')
    },
    watch: {
      currentGStep (newVal, oldVal) {
        console.log(newVal)
        if (!newVal) {
          return
        }
        if (newVal.action === 'search') {
          this.searchRenderer.setSearchLayer(newVal)
          return
        }
        if (oldVal.action === 'search' && newVal.action === 'grow') {
          this.map.removeLayer(this.searchRenderer.layers)
          this.growRenderer = new CountyLayer()
          this.map.addLayer(this.growRenderer.layers)
        }
      }
    }
  }
</script>

<style lang="sass" scoped>
#map2
  height: calc(100vh - 71px)
  width: 100%

</style>
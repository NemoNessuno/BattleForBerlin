<template>
  <div id="map2" />
</template>
<script>
  import {buildLeafletMap} from '../helpers'
  import {AnimationLayer} from '../layers'
  import {mapState, mapGetters} from 'vuex'
  export default {
    name: 'animation-map',
    data () {
      return {
        animationIndex: 0,
        animationRenderer: undefined
      }
    },
    created () {
      if (!this.gActive) {
        this.$router.push('/map')
      }
    },
    computed: {
      ...mapState(['gActive', 'districtHash']),
      ...mapGetters(['counties'])
    },
    mounted () {
      this.map = buildLeafletMap(this.$el)
      this.animationRenderer = new AnimationLayer(this.districtHash, this.counties)
      this.animationRenderer.layers.addTo(this.map)
      this.animationRenderer.run()
    }
  }
</script>

<style lang="sass" scoped>
#map2
  height: calc(100vh - 71px)
  width: 100%

</style>
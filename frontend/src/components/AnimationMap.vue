<template>
  <div id="map2" />
</template>
<script>
  import {buildLeafletMap} from '../helpers'
  import {AnimationLayer} from '../layers'
  import {mapState} from 'vuex'
  export default {
    name: 'animation-map',
    data () {
      return {
        animationIndex: 0
      }
    },
    created () {
      if (!this.$store.state.animationActive) {
        this.$router.push('/map')
      }
    },
    computed: {
      ...mapState(['gerrymanderAnimation', 'districtHash', 'animationActive', 'gsteps']),
      stop () {
        if (!this.gsteps || this.gsteps.length > this.animationIndex + 1) {
          return false
        }
        return this.animationIndex + 1 === this.gstep
      }
    },
    mounted () {
      this.map = buildLeafletMap(this.$el)
      this.renderer = new AnimationLayer(this.districtHash)
      this.renderer.runAnimation(this.gerrymanderAnimation)
      this.renderer.layers.addTo(this.map)
    }
  }
</script>

<style lang="sass" scoped>
#map2
  height: calc(100vh - 71px)
  width: 100%

</style>
<template>
  <div id="map2" />
</template>
<script>
  import 'rxjs/add/operator/distinctUntilChanged'
  import 'rxjs/add/operator/takeWhile'
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
      this.animationRenderer.status.distinctUntilChanged().takeWhile(action => action !== 'stop').subscribe(
        status => this.$store.commit('setGStatus', status),
        console.error,
        () => {
          this.$store.commit('setGStatus', undefined)
          this.$store.dispatch('loadCounties').then(() => this.$router.push('/map'))
          this.$store.dispatch('loadDiffCount')
        }
      )
    }
  }
</script>

<style lang="sass" scoped>
#map2
  height: calc(100vh - 71px)
  width: 100%

</style>
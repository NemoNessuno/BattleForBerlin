<template>
  <div id="map2" />
</template>
<script>
  import {buildLeafletMap} from '../helpers'
  export default {
    name: 'animation-map',
    data () {
      return {
      }
    },
    mounted () {
      this.map = buildLeafletMap(this.$el)
    }
  }
</script>

<style lang="sass" scoped>
#map2
  height: 600px
  width: 100%

</style>
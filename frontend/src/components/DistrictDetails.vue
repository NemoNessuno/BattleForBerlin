<template>
  <map-overlay :result="currentDistrict.result" >
    <v-toolbar slot="title" extended dense card>
      <v-btn icon to="/map">
        <v-icon>close</v-icon>
      </v-btn>
      <v-toolbar-title>Wahlbezirk {{districtId}}</v-toolbar-title>
      <template slot="extension">
        <v-toolbar-title class="subheading" >{{bezirk}}</v-toolbar-title>
      </template>
    </v-toolbar>
    <select-bwk
      :bwk="bwk"
      :identifier="districtId"
      />
  </map-overlay>
</template>

<script>
  import MapOverlay from './MapOverlay'
  import SelectBwk from './SelectBWK'
  import {mapState} from 'vuex'
  import {BWK_NAMES} from '@/helpers'
  export default {
    name: 'DistrictDetails',
    data () {
      return {
        dialog: false
      }
    },
    computed: {
      bwk () { return this.currentDistrict.bwk || '' },
      districtId () { return this.currentDistrict.identifier || '' },
      bezirk () { return BWK_NAMES[this.bwk] },
      ...mapState(['districtProps']),
      currentDistrict () {
        return this.districtProps[this.$route.params.identifier]
      }
    },
    components: {MapOverlay, SelectBwk}
  }
</script>

<style scoped>
h3.headline, h4.subheading {
  width: 100%;
}
</style>

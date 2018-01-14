<template>
  <map-overlay :result="currentDistrict.result" @close="close">
    <v-toolbar slot="title" extended dense card>
      <v-btn icon @click.native="unselectItem">
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
  import {mapGetters, mapMutations} from 'vuex'
  import {BWK_NAMES} from '@/helpers'
  export default {
    name: 'DistrictDetails',
    props: {
      district: {type: Object, required: true}
    },
    data () {
      return {
        dialog: false
      }
    },
    computed: {
      bwk () { return this.currentDistrict.bwk || '' },
      districtId () { return this.currentDistrict.identifier || '' },
      bezirk () { return BWK_NAMES[this.bwk] },
      ...mapGetters(['currentDistrict'])
    },
    methods: mapMutations(['unselectItem']),
    components: {MapOverlay, SelectBwk}
  }
</script>

<style scoped>
h3.headline, h4.subheading {
  width: 100%;
}
</style>

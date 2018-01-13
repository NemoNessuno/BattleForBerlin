<template>
  <map-overlay :result="district.result" @close="close">
    <v-toolbar slot="title" extended dense card>
      <v-btn icon @click.native="close">
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
  import closeActionMixin from '@/mixins/closeActionMixin'
  import MapOverlay from './MapOverlay'
  import SelectBwk from './SelectBWK'
  import {BWK_NAMES} from '@/helpers'
  export default {
    name: 'DistrictDetails',
    props: {
      district: {type: Object, required: true}
    },
    mixins: [closeActionMixin],
    data () {
      return {
        dialog: false
      }
    },
    computed: {
      bwk () { return this.district.bwk || '' },
      districtId () { return this.district.identifier || '' },
      bezirk () { return BWK_NAMES[this.district.bwk] }
    },
    components: {MapOverlay, SelectBwk}
  }
</script>

<style scoped>
h3.headline, h4.subheading {
  width: 100%;
}
</style>

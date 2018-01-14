<template>
  <map-overlay :result="currentDistrict.result" @close="unselectItem">
    <v-toolbar dark slot="title" >
      <v-btn icon @click.native="close">
        <v-icon>close</v-icon>
      </v-btn>
      <v-toolbar-title>{{currentDistrict.bwk}} - {{bezirk}}</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn icon @click.native="dialog = true">
        <v-icon>poll</v-icon>
      </v-btn>
    </v-toolbar>
  </map-overlay>
</template>

<script>
import MapOverlay from './MapOverlay'
import GerryMander from './GerryMander'
import {BWK_NAMES} from '@/helpers'
import {mapGetters, mapMutations} from 'vuex'
export default {
  name: 'county-details',
  computed: {
    bezirk () {
      return BWK_NAMES[this.currentDistrict.bwk]
    },
    ...mapGetters(['currentDistrict'])
  },
  methods: mapMutations(['unselectItem']),
  components: {MapOverlay, GerryMander}
}
</script>
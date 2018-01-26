<template>
  <map-overlay :result="currentCounty.result" @close="unselectItem">
    <v-toolbar dark slot="title" >
      <v-btn icon @click.native="unselectItem">
        <v-icon>close</v-icon>
      </v-btn>
      <v-toolbar-title>{{currentCounty.bwk}} - {{bezirk}}</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn icon :to="'/votingdistrict/' + currentCounty.bwk">
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
      return BWK_NAMES[this.currentCounty.bwk]
    },
    ...mapGetters(['currentCounty'])
  },
  methods: mapMutations(['unselectItem', 'goToGerryMander']),
  components: {MapOverlay, GerryMander}
}
</script>
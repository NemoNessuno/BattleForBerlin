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
import {mapState, mapMutations} from 'vuex'
export default {
  name: 'county-details',
  computed: {
    ...mapState(['countyProps']),
    bezirk () {
      return BWK_NAMES[this.currentCounty.bwk]
    },
    currentCounty () {
      return this.countyProps[this.$route.params.identifier]
    }
  },
  methods: mapMutations(['unselectItem', 'goToGerryMander']),
  components: {MapOverlay, GerryMander}
}
</script>
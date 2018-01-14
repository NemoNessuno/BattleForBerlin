<template>
  <div>
    <v-toolbar class="primary">
      <v-btn icon @click.native="setGerryManderVisible(false)">
        <v-icon>close</v-icon>
      </v-btn>
      <v-toolbar-title>
        {{currentCounty.bwk}} - {{bezirk}}
      </v-toolbar-title>
    </v-toolbar>
    <v-container grid-list-md>
      <v-layout row wrap>
        <candidate v-for="candidate of candidates" :candidate="candidate" :key="'can.' + candidate.name">
        </candidate>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
import Candidate from './Candidate'
import {mapState, mapGetters, mapMutations} from 'vuex'
import {BWK_NAMES} from '@/helpers'
export default {
  name: 'gerry-mander',
  computed: {
    ...mapState(['gerryManderVisible']),
    ...mapGetters(['currentCounty']),
    bezirk () { return BWK_NAMES[this.currentCounty.bwk] },
    candidates () {
      return Object.keys(this.currentCounty.candidates).map(function (party) {
        return this.currentCounty.candidates[party]
      }.bind(this))
    }
  },
  methods: mapMutations(['setGerryManderVisible']),
  components: {Candidate}
}
</script>
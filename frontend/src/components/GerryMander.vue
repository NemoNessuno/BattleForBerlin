<template>
  <div>
    <v-toolbar class="primary">
      <v-btn icon @click.native="goToMap">
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
import {mapGetters, mapMutations} from 'vuex'
import {BWK_NAMES} from '@/helpers'
export default {
  name: 'gerry-mander',
  computed: {
    ...mapGetters(['currentCounty']),
    bezirk () { return BWK_NAMES[this.currentCounty.bwk] },
    candidates () {
      return Object.keys(this.currentCounty.candidates).map(function (party) {
        const candidate = this.currentCounty.candidates[party]
        candidate.votes = this.currentCounty.result[party]
        return candidate
      }.bind(this))
    }
  },
  methods: mapMutations(['goToMap']),
  components: {Candidate}
}
</script>
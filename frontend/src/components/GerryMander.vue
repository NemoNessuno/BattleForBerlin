<template>
  <div>
    <v-toolbar class="primary">
      <v-btn icon to="/map">
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
import {BWK_NAMES} from '@/helpers'
export default {
  name: 'gerry-mander',
  mounted () {
    console.log(this.$route.params)

  },
  computed: {
    bezirk () { return BWK_NAMES[this.bwk] },
    candidates () {
      let candidateList = Object.keys(this.currentCounty.candidates).map(function (party) {
        const candidate = {...this.currentCounty.candidates[party]}
        candidate.votes = this.currentCounty.result[party]
        return candidate
      }.bind(this)).sort(function (a, b) { return b.votes - a.votes })
      candidateList = candidateList.map(function (candidate, index) {
        candidate.winner = index === 0
        candidate.total = this.total
        return candidate
      }.bind(this))
      return candidateList
    },
    bwk () {
      console.log(this.$route)
      return this.$route.params.identifier
    }
  },
  components: {Candidate}
}
</script>

<style lang="sass" scoped>
.summary
  margin: 1em auto
  padding: 0.7em
  width: 95%
</style>
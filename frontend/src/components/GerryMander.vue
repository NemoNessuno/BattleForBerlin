<template>
  <div>
    <v-toolbar class="primary">
      <v-btn icon to="/map">
        <v-icon>close</v-icon>
      </v-btn>
      <v-toolbar-title>
        {{bwk}} - {{bezirk}}
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
import {mapState} from 'vuex'
export default {
  name: 'gerry-mander',
  computed: {
    ...mapState(['countyProps']),
    bezirk () { return BWK_NAMES[this.bwk] },
    ready () {
      return Boolean(this.countyProps)
    },
    candidates () {
      if (!this.ready) {
        return
      }
      let candidateList = Object.keys(this.countyProps[this.bwk].candidates).map(function (party) {
        const candidate = {...this.countyProps[this.bwk].candidates[party]}
        candidate.votes = this.countyProps[this.bwk].result[party]
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
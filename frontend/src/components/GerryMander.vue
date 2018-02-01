<template>
  <div>
    <v-toolbar class="primary">
      <v-btn icon to="/map" :disabled="Boolean(gerrymanderCandidate)">
        <v-icon>close</v-icon>
      </v-btn>
      <v-toolbar-title>
        {{bwk}} - {{bezirk}}
      </v-toolbar-title>
    </v-toolbar>
    <transition name="zoom-in" mode="out-in">
      <div v-if="ready">
        <transition name="zoom-in" mode="out-in" >
          <v-container grid-list-md v-if="!gerrymanderCandidate">
            <v-layout row wrap>
              <candidate
                v-for="candidate of candidates"
                :candidate="candidate"
                :key="'can.' + candidate.name"
                @gerrymander="gerrymander"
                >
              </candidate>
            </v-layout>
          </v-container>
          <div class="spinning-candidate" v-else>
            <candidate :candidate="gerrymanderCandidate" :waiting="true" />
          </div>
        </transition>
      </div>
      <div v-else class="waiting">
        <v-progress-circular :indeterminate="true" :size="120" :width="5" />
      </div>
    </transition>
  </div>
</template>

<script>
import Candidate from './Candidate'
import {BWK_NAMES} from '@/helpers'
import {mapState} from 'vuex'
export default {
  name: 'gerry-mander',
  data () {
    return {
      gerrymanderParty: undefined
    }
  },
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
    },
    gerrymanderCandidate () {
      if (!this.gerrymanderParty) {
        return undefined
      }
      const candidate = {...this.countyProps[this.bwk].candidates[this.gerrymanderParty]}
      candidate.votes = this.countyProps[this.bwk].result[this.gerrymanderParty]
      return candidate
    }
  },
  methods: {
    gerrymander (payload) {
      const waitFor = this.$store.dispatch('gerrymander', payload)
      this.gerrymanderParty = payload.party
      this.$store.commit('setAnimationActive', true)
      waitFor.then(() => {
        this.$router.push('/animation')
      })
    }
  },
  components: {Candidate}
}
</script>

<style lang="sass" scoped>
.waiting
  display: flex
  justify-content: center

.spinning-candidate
  margin-top: 5em
  display: flex
  justify-content: center

.zoom-in-enter, .zoom-in-leave-to
  transform: scale(0.3)
  opacity: 0.5

.zoom-in-enter-to, .zoom-in-leave
  transform: scale(1)
  opacity: 1

.zoom-in-enter-active, .zoom-in-leave-active
  transition: all .8s ease

</style>
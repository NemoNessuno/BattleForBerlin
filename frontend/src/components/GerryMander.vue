<template>
<v-dialog
  v-model="gerryManderVisible"
  fullscreen
  transition="dialog-bottom-transition"
  :overlay="false">
  <v-card>
    <v-toolbar class="primary">
      <v-btn icon>
        <v-icon>close</v-icon>
      </v-btn>
      <v-toolbar-title>
        {{district.bwk}} - {{bezirk}}
      </v-toolbar-title>
    </v-toolbar>
    <v-container grid-list-md>
      <v-layout row wrap>
        <candidate v-for="candidate of candidates" :candidate="candidate" :key="'can.' + candidate.name">
        </candidate>
      </v-layout>
    </v-container>
  </v-card>
</v-dialog>

</template>

<script>
import Candidate from './Candidate'
import {mapState, mapGetters} from 'vuex'
export default {
  name: 'gerry-mander',
  computed: {
    ...mapState(['gerryManderVisible']),
    ...mapGetters(['currentCounty']),
    candidates () {
      Object.keys(this.currentCounty.candidates).map(function (party) {
        return this.currentCounty.candidates[party]
      }.bind(this))
    }
  },
  components: {Candidate}
}
</script>
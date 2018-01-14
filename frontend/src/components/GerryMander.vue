<template>
<v-dialog
  v-model="visible"
  fullscreen
  transition="dialog-bottom-transition"
  :overlay="false">
  <v-card>
    <v-toolbar class="primary">
      <v-btn icon @click.native="close">
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
import closeActionMixin from '@/mixins/closeActionMixin'
import Candidate from './Candidate'
export default {
  name: 'gerry-mander',
  mixins: [closeActionMixin],
  props: {
    district: {type: Object, required: true},
    visible: {type: Boolean, required: true}
  },
  computed: {
    candidates () {
      Object.keys(this.district.candidates).map(function (party) {
        return this.district.candidates[party]
      }.bind(this))
    }
  },
  components: {Candidate}
}
</script>
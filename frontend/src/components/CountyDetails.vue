<template>
  <map-overlay :result="district.result" @close="close">
    <v-toolbar dark slot="title" card>
      <v-btn icon>
        <v-icon>close</v-icon>
      </v-btn>
      <v-toolbar-title>{{district.bwk}} - {{bezirk}}</v-toolbar-title>
    </v-toolbar>
  </map-overlay>
</template>

<script>
import MapOverlay from './MapOverlay'
import {BWK_NAMES} from '@/helpers'
export default {
  name: 'county-details',
  props: {district: {type: Object, required: true}},
  computed: {
    bezirk () {
      return BWK_NAMES[this.district.bwk]
    }
  },
  components: {MapOverlay}
}
</script>
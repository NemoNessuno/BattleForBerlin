<template>
  <div class="detail-wrapper">
    <v-card class="elevation-12" primary-title>
      <v-card-title class="overlay-title">
        <slot name="title" />
      </v-card-title>
      <v-card-text>
        <slot></slot>
        <stacked-bar-chart :result="result" />
        <v-data-table
          :headers="headers"
          :items="results"
          hide-actions>
          <template slot="items" slot-scope="props">
            <td v-if="props.item.winner" style="font-weight: bold"> {{props.item.name}}</td>
            <td v-if="!props.item.winner"> {{props.item.name}}</td>
            <td v-if="props.item.winner" style="font-weight: bold"> {{props.item.result}}</td>
            <td v-if="!props.item.winner">{{props.item.result}}</td>
          </template>
        </v-data-table>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn @click.native="close">Close</v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
import {maxProp} from '@/helpers'
import StackedBarChart from './StackedBarChart'
export default {
  mame: 'map-overlay',
  props: {result: {type: Object, required: true}},
  data () {
    return {
      headers: [
        {text: 'Partei', align: 'left', value: 'name'},
        {text: 'Stimmen', align: 'right', value: 'result'}
      ]
    }
  },
  computed: {
    winner () { return maxProp(this.result) },
    results () {
      return [
        {name: 'CDU', result: this.result.cdu, winner: this.winner === 'cdu'},
        {name: 'SPD', result: this.result.spd, winner: this.winner === 'spd'},
        {name: 'Die Grünen', result: this.result.gruene, winner: this.winner === 'gruene'},
        {name: 'AFD', result: this.result.afd, winner: this.winner === 'afd'},
        {name: 'FDP', result: this.result.fdp, winner: this.winnner === 'fdp'},
        {name: 'Die Linke', result: this.result.die_linke, winner: this.winner === 'die_linke'}
      ]
    }
  },
  methods: {
    close () {
      this.$emit('close')
    }
  },
  components: {StackedBarChart}
}
</script>

<style lang="sass" scoped>
h3.headline, h4.subheading
  width: 100%

.winner
  font-weight: bold

.detail-wrapper
  position: absolute
  left: 1em
  width: 30em
  z-index: 1000
  @media(min-height: 800px)
    top: 10em
  @media(max-height: 800px)
    top: 8em
    height: 37em
    overflow-y: scroll
  .overlay-title
    padding: 0
</style>
<template>
  <div class="interactive-select">
    <v-select
      :items="items"
      label="Wahlbezirk"
      v-model="value"
      >
    </v-select>
    <v-progress-linear :indeterminate="true" v-if="waiting" style="height: 3px" ></v-progress-linear>
  </div>
</template>

<script>
import {store} from '@/backend'
import {minAwait} from '@/helpers'
import {Observable} from 'rxjs/Observable'
import 'rxjs/add/observable/fromPromise'
export default {
  name: 'select-bwk',
  props: {bwk: {type: String, required: true}, identifier: {type: String, required: true}},
  data () {
    return {
      value: this.bwk,
      waiting: false,
      done: false,
      timeout: undefined,
      items: [
        {text: '075 - Mitte', value: '075'},
        {text: '076 - Pankow', value: '076'},
        {text: '077 - Reinickendorf', value: '077'},
        {text: '078 - Spandau', value: '078'},
        {text: '079 - Steglitz/Zehlendorf', value: '079'},
        {text: '080 - Charlottenburg/Wilmersdorf', value: '080'},
        {text: '081 - Tempelhof/Schöneberg', value: '081'},
        {text: '082 - Neukölln', value: '082'},
        {text: '083 - Friedrichshain/Kreuzb.', value: '083'},
        {text: '084 - Treptow/Köpenick', value: '084'},
        {text: '085 - Marzahn/Hellersdorf', value: '085'},
        {text: '086 - Lichtenberg', value: '086'}
      ]
    }
  },
  watch: {
    value (newVal) {
      this.waiting = true
      const fetcher = Observable.fromPromise(store.changeDistrict(this.identifier, newVal))
      minAwait(fetcher).subscribe(
        function () { this.waiting = false }.bind(this),
        function (error) {
          this.waiting = false
          console.log('Failed changing district')
          console.error(error)
        }.bind(this)
      )
    }
  }
}
</script>

<style lang="sass" scoped>
.interactive-select
  height: 9em

.fade-enter-active, .fade-leave-active
  transition: opacity 0.3s

.fade-enter, .fade-leave-to
  opacity: 0
</style>
<template>
  <div class="interactive-select">
    <v-select
      :items="items"
      label="Wahlbezirk"
      v-model="value"
      @change="changeBwk"
      >
    </v-select>
    <v-progress-linear :indeterminate="true" v-if="waiting" style="height: 3px" ></v-progress-linear>
  </div>
</template>

<script>
import {store} from '@/backend'
import {minAwait, BWK_NAMES} from '@/helpers'
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
      items: Object.keys(BWK_NAMES).map(function (key) {
        return {value: key, text: key + ' - ' + BWK_NAMES[key]}
      })
    }
  },
  methods: {
    changeBwk (val) {
      this.waiting = true
      const fetcher = Observable.fromPromise(store.changeDistrict(this.identifier, val))
      minAwait(fetcher).subscribe(
        function () { this.waiting = false }.bind(this),
        function (error) {
          this.waiting = false
          console.log('Failed changing district')
          console.error(error)
        }.bind(this)
      )
    }
  },
  watch: {
    bwk (newVal) {
      this.value = newVal
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
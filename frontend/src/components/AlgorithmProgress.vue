<template>
  <div class="algorithm-progress">
    <div class="left-side">
      <v-progress-linear
        :indeterminate="indeterminate"
        :value="progress"
        />
    </div>
    <div class="right-side">

    </div>
  </div>
</template>

<script>
import {mapState} from 'vuex'
export default {
  name: 'algorithm-progress',
  computed: {
    ...mapState(['algorithmProgress']),
    indeterminate () {
      return this.algorithmProgress.totalShifts === 0
    },
    progress () {
      const val = this.algorithmProgress.shifts / this.algorithmProgress.totalShifts
      return Math.round(val) * 100
    },
    status () {
      if (!this.algorithmProgress.reset) {
        return 'resetting'
      }
      if (this.algorithmProgress.reset && this.indeterminate) {
        return 'resetted'
      }
      return this.algorithmProgress.shifts + ' of ' + this.algorithmProgress.totalShifts + ' districts changed'
    }
  }
}
</script>

<style lang="sass">
.algorithm-progress
  width: 100%
  display: flex
  .left-side
    width: 40%
  .right-side
    width: 45%
</style>

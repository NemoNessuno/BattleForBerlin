<template>
  <div class="algorithm-progress">
    <div class="left-side">
      <v-progress-linear
        :indeterminate="indeterminate"
        :value="progress"
        :color="color"
        style="margin: 6px 10px 0  10px"
        />
    </div>
    <div class="right-side">
      {{status}}
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
      return this.algorithmProgress.totalShifts === 0 || this.algorithmProgress.shifts === 0
    },
    progress () {
      const val = this.algorithmProgress.shifts / this.algorithmProgress.totalShifts
      return Math.round(val * 100)
    },
    color () {
      if (this.progress === 100) {
        return 'success'
      }
      return 'info'
    },
    status () {
      if (!this.algorithmProgress.reset) {
        return 'resetting'
      }
      if (this.algorithmProgress.reset && this.indeterminate) {
        return 'resetted'
      }
      const shifts = this.algorithmProgress.shifts || '0'
      return shifts + ' of ' + this.algorithmProgress.totalShifts + ' districts changed'
    }
  }
}
</script>

<style lang="sass">
.algorithm-progress
  width: 100%
  height: 16px
  display: flex
  .left-side
    width: 40%
  .right-side
    width: 45%
    line-height: 16px
    padding-left: 2em
</style>

<template>
<div class="bar-wrapper">
  <div class="party-result"
    v-for="(party, index) of sortedResult"
    :class="party.party"
    :style="{width: party.width}"
    :key="'bar.' + party.party"
    >
    <span v-if="party.percentage > 10" class="percentage">
      {{Math.round(party.percentage)}}%
    </span>
    </div>
</div>

</template>
<script>
export default {
  name: 'stacked-bar-chart',
  props: {result: {type: Object, required: true}},
  computed: {
    totalVotes () {
      return Object.keys(this.result).map(key => this.result[key]).reduce((acc, val) => acc + val, 0)
    },
    sortedResult () {
      let list = Object.keys(this.result).map(key => {
        const result = {votes: this.result[key], party: key}
        result.percentage = (result.votes / this.totalVotes) * 100
        return result
      }).sort(function (a, b) {
        if (a.votes < b.votes) {
          return 1
        } else if (a.votes === b.votes) {
          return 0
        } else {
          return -1
        }
      })
      const total = list.slice(0, 5).reduce(function (acc, item) { return acc + item.percentage }, 0)
      list[5].percentage = 100 - total
      list = list.map(function (item) {
        item.width = item.percentage + '%'
        return item
      })
      return list
    }
  }
}
</script>

<style lang="sass" scoped>
.bar-wrapper
  height: 2.5em
  line-height: 2.5em
  width: 100%

.party-result
  display: inline-block
  height: 100%
  transition: width 0.3s ease
  text-align: right
  padding-right: 2px
  vertical-align: top
</style>

<template>
<div class="bar-wrapper"><div
:style="cdu" class="party-result"
/><div
:style="spd"
class="party-result" /><div
:style="gruene"
class="party-result" /><div
class="party-result"
:style="fdp" /><div
class="party-result"
:style="linke" /><div
class="party-result"
:style="afd" />
</div>

</template>
<script>
import {PARTY_COLORS} from '@/helpers'
export default {
  name: 'stacked-bar-chart',
  props: {result: {type: Object, required: true}},
  computed: {
    totalVotes () {
      return Object.keys(this.result).map(key => this.result[key]).reduce((acc, val) => acc + val, 0)
    },
    percentages () {
      const vals = {}
      let totals = 0
      Object.keys(this.result).forEach(key => {
        vals[key] = Math.round((this.result[key] / this.totalVotes) * 1000) / 10
        totals += vals[key]
      })
      if (totals > 100) {
        vals.afd = vals.afd - (totals - 100)
      }
      return vals
    },
    cdu () {
      return {
        width: this.percentages.cdu + '%',
        'background-color': PARTY_COLORS.cdu
      }
    },
    spd () {
      return {
        width: this.percentages.spd + '%',
        'background-color': PARTY_COLORS.spd
      }
    },
    gruene () {
      return {
        width: this.percentages.gruene + '%',
        'background-color': PARTY_COLORS.gruene
      }
    },
    fdp () {
      return {
        width: this.percentages.fdp + '%',
        'background-color': PARTY_COLORS.fdp
      }
    },
    linke () {
      return {
        width: this.percentages.die_linke + '%',
        'background-color': PARTY_COLORS.die_linke
      }
    },
    afd () {
      return {
        width: this.percentages.afd + '%',
        'background-color': PARTY_COLORS.afd
      }
    }
  }
}
</script>

<style scoped>
.bar-wrapper {
  height: 2em;
}
.party-result {
  height: 2em;
  display: inline-block;
  transition: width 0.3s ease;

}
</style>

<template>
  <v-flex md3>
    <v-card>
      <v-toolbar :class="candidate.party">
        <v-toolbar-title>
          {{partyTitle }}
        </v-toolbar-title>
      </v-toolbar>
      <v-card-text class="white" style="color: black">
        <v-avatar size="64px">
          <img v-bind:src="candidate.image" alt="candidate.name" />
        </v-avatar>
          {{candidate.name}}
      </v-card-text>
    </v-card>
  </v-flex>
</template>

<script>
  import {PARTY_COLORS} from '@/helpers'
  const PARTY_NAMES = {
    cdu: 'CDU',
    spd: 'SPD',
    gruene: 'Bündnis 90/Die Grünen',
    die_linke: 'Die Linke',
    afd: 'AfD',
    fdp: 'FDP'
  }
  export default {
    name: 'candidate',
    props: {
      candidate: {type: Object, required: true}
    },
    computed: {
      partyColor () {
        return PARTY_COLORS[this.candidate.party]
      },
      partyTitle () {
        return PARTY_NAMES[this.candidate.party]
      }
    }
  }
</script>

<style scoped>

</style>
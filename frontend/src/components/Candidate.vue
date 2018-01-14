<template>
  <v-flex md3>
    <v-card>
      <v-toolbar :style="{'background-color': partyColor}">
        {{candidate.name}} ({{candidate.party}})
      </v-toolbar>
      <v-card-text>
        <v-avatar size="48px">
          <img v-bind:src="candidate.image" alt="description.name" />
        </v-avatar>
      </v-card-text>
    </v-card>
  </v-flex>
</template>

<script>
  import {PARTY_COLORS} from '@/helpers'
  export default {
    name: 'candidate',
    props: {
      candidate: {type: Object, required: true}
    },
    computed: {
      partyColor () {
        return PARTY_COLORS[this.candidate.party]
      }
    }
  }
</script>

<style scoped>

</style>
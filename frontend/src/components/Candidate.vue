<template>
  <v-flex md4>
    <v-card>
      <v-toolbar :class="candidate.party">
        <v-toolbar-title>
          {{partyTitle }}
        </v-toolbar-title>
      </v-toolbar>
      <v-card-text class="white black--text" style="color: black">
        <v-list class="white" style="color: black">
          <v-list-tile avatar>
            <v-list-tile-avatar>
              <img v-bind:src="candidate.image" alt="candidate.name" />
            </v-list-tile-avatar>
            <v-list-tile-content style="color: black">
              {{candidate.name}}
            </v-list-tile-content>
          </v-list-tile>
        </v-list>
          {{questions}} {{answers}}
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
    data () {
      return {
        questions: 0,
        answers: 0,
        error: false
      }
    },
    mounted () {
      const $this = this
      if (this.candidate.description && this.candidate.name === 'Frank Henkel') {
        let desc = this.candidate.description.replace('https://www.abgeordnetenwatch.de/api/parliament/bundestag/profile/', '')
        desc = desc.replace('/profile.json', '')
        fetch('/api/candidate/' + desc)
          .then(resp => resp.json())
          .then(({profile}) => {
            $this.questions = profile.meta.questions
            $this.answers = profile.meta.answers
          })
          .catch((error) => {
            $this.error = true
          })
      }
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

<style lang="sass" scoped>
img 
  object-fit: cover
</style>
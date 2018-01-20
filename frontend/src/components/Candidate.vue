<template>
  <v-flex md6 lg4>
    <v-card>
      <v-toolbar :class="candidate.party">
        <v-toolbar-title>
          {{partyTitle }}
        </v-toolbar-title>
        <v-spacer>
        </v-spacer>
        <v-tooltip bottom>
          <v-btn
            icon
            :class="candidate.party"
            :href="candidate.profile_url"
            tag="a"
            slot="activator"
            target="_blank">
            <v-icon>open_in_new</v-icon>
          </v-btn>
          <span>Profil auf Abgeordnetenwatch</span>
        </v-tooltip>
      </v-toolbar>
      <v-card-text class="white black--text" >
        <v-list class="white">
          <v-list-tile avatar>
            <v-list-tile-avatar>
              <img v-bind:src="candidate.image" alt="candidate.name" />
            </v-list-tile-avatar>
            <v-list-tile-content style="color: black" class="headline">
              {{candidate.name}}
            </v-list-tile-content>
          </v-list-tile>
        </v-list>
        <v-divider></v-divider>
        <v-list>
          <v-list-tile avatar>
            <v-list-tile-avatar style="color:black">
              <v-icon>question_answer</v-icon>
            </v-list-tile-avatar>
            <v-list-tile-content>
              <v-list-tile-title>
                <span v-if="!loaded">
                  fetching
                </span>
                <span v-if="loaded && error">
                  failed
                </span>
                <span v-if="loaded && !error">
                  {{answered}} % der Fragen beantwortet
                </span>
              </v-list-tile-title>
              <v-list-tile-sub-title>
                <v-progress-linear :indeterminate="true" v-if="!loaded" />
                <v-progress-linear v-model="answered" v-else />
              </v-list-tile-sub-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list>
      </v-card-text>
      <v-card-actions class="white">
        <v-spacer />
        <v-btn
          flat
          :disabled="candidate.winner"
          @click.native="run"
          class="orange--text">
          Lass mich gewinnen!
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-flex>
</template>

<script>
  import {mapMutations, mapActions} from 'vuex'
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
        error: false,
        loaded: false
      }
    },
    mounted () {
      const $this = this
      if (this.candidate.description) {
        let desc = this.candidate.description.replace('https://www.abgeordnetenwatch.de/api/parliament/bundestag/profile/', '')
        desc = desc.replace('/profile.json', '')
        fetch('/api/candidate/' + desc)
          .then(resp => resp.json())
          .then(({profile}) => {
            $this.questions = profile.meta.questions
            $this.answers = profile.meta.answers
            $this.loaded = true
          })
          .catch((error) => {
            console.error(error)
            $this.error = true
            $this.loaded = true
          })
      }
    },
    computed: {
      partyColor () {
        return PARTY_COLORS[this.candidate.party]
      },
      partyTitle () {
        return PARTY_NAMES[this.candidate.party]
      },
      answered () {
        if (this.answers === 0) {
          return 0
        }
        return Math.round(this.answers / this.questions) * 100
      }
    },
    methods: {
      ...mapActions(['gerryMander']),
      ...mapMutations(['goToMap']),
      run () {
        this.gerryMander({
          bwk: this.candidate.bwk,
          party: this.candidate.party
        })
        this.goToMap()
      }
    }
  }
</script>

<style lang="sass" scoped>
img
  object-fit: cover
</style>
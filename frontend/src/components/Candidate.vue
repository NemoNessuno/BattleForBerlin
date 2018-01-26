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
              <img v-bind:src="candidate.image" alt="candidate.name" v-if="showImage" />
            </v-list-tile-avatar>
            <v-list-tile-content style="color: black" class="headline">
              {{degree}} {{candidate.name}}
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile avatar>
            <v-list-tile-avatar :class="textClass">
              <v-icon class="black--text">sort</v-icon>
            </v-list-tile-avatar>
            <v-list-tile-content :class="textClass">
              {{ranking}}
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile>
            <v-list-tile-avatar :class="textClass">
              <v-icon class="black--text">school</v-icon>
            </v-list-tile-avatar>
            <v-list-tile-content :class="textClass">
              {{educationString}}
            </v-list-tile-content>
          </v-list-tile>
        </v-list>
        <div class="waiting" v-if="waiting">
          <div>
          <v-progress-circular :size="200" :width="5" color="blue" :indeterminate="true" />
          <p class="title black--text status-text" >
            Berechne Bezirke
          </p>
          </div>
        </div>
      </v-card-text>
      <v-card-actions class="white" v-if="!waiting">
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
      candidate: {type: Object, required: true},
      waiting: {type: Boolean, default: false}
    },
    data () {
      return {
        error: false,
        loaded: false,
        rank: undefined,
        degree: '',
        education: '',
        showImage: false
      }
    },
    mounted () {
      window.setTimeout(function () {
        this.showImage = true
      }.bind(this), Math.round(Math.random() * 500))
      const $this = this
      if (this.candidate.description) {
        let desc = this.candidate.description.replace('https://www.abgeordnetenwatch.de/api/parliament/bundestag/profile/', '')
        desc = desc.replace('/profile.json', '')
        fetch('/api/candidate/' + desc)
          .then(resp => resp.json())
          .then(({profile}) => {
            $this.rank = parseInt(profile.list.position)
            $this.degree = profile.personal.degree
            $this.education = profile.personal.education
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
      ranking () {
        if (!this.loaded) {
          return 'lade ...'
        }
        if (this.loaded && this.rank) {
          return 'Listenplatz ' + this.rank
        }
        return 'ohne Listenplatz'
      },
      educationString () {
        if (!this.loaded) {
          return 'lade ...'
        }
        if (!this.education) {
          return 'unbekannt'
        }
        if (this.education.length < 50) {
          return this.education
        }
        return this.education.substring(0, 49) + '...'
      },
      textClass () {
        if (this.loaded) {
          return 'black--text'
        }
        return 'grey--text'
      }
    },
    methods: {
      run () {
        this.$emit('gerrymander', {bwk: this.candidate.bwk, party: this.candidate.party})
      }
    }
  }
</script>

<style lang="sass" scoped>
@keyframes pulsation
  from
    opacity: 0.5
  to
    opacity: 0.95
img
  object-fit: cover
.waiting
  display: flex
  justify-content: center
  text-align: center
  p.status-text
    margin-top: 0.5em
    animation-name: pulsation
    animation-duration: 1.5s
    animation-direction: alternate
    animation-iteration-count: infinite
    animation-timing-function: ease
</style>
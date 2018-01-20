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
              {{candidate.name}}
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile avatar>
            <v-list-tile-avatar class="black--text">
              <v-icon class="black--text">sort</v-icon>
            </v-list-tile-avatar>
            <v-list-tile-content class="black--text">
              <span v-if="!loaded">
                fetching
              </span>
              <span v-else-if="loaded && rank">
                Listenplatz {{rank}}
              </span>
              <span v-else>
                Listenplatz unbekannt
              </span>
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
        error: false,
        loaded: false,
        rank: undefined,
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
<template>
  <v-app id="bfb" dark>
    <v-toolbar app fixed clipped-left>
      <v-toolbar-title>
        Battle For Berlin
      </v-toolbar-title>
      <v-spacer />
      <v-toolbar-items class="hidden-sm-and-down">
        <v-btn @click="route = 'onboarding'" icon large v-if="route === 'map'">
          <v-icon>info_outline</v-icon>
        </v-btn>
        <v-btn @click="route = 'map'" icon large v-if="route === 'onboarding'">
          <v-icon>map</v-icon>
        </v-btn>
        <v-btn href="https://github.com/NemoNessuno/BattleForBerlin" flat>
          <img src="/static/images/github_logo.png" class="github-link-img" />
        </v-btn>
      </v-toolbar-items>
    </v-toolbar>
    <v-content>
      <onboarding v-if="route === 'onboarding'" @skip="skipOnboarding" />
      <leaflet-map v-if="route === 'map'" :uwb="urnenWahlbezirke || []" :lwb="briefWahlbezirke || []" />
    </v-content>
    <v-footer>
      <span>&copy; 2017, S&ouml;ren Titze, Christian Windolf</span>
    </v-footer>
  </v-app>
</template>

<script>
import Onboarding from './components/Onboarding'
import LeafletMap from './components/LeafletMap'
export default {
  name: 'app',
  data () {
    return {
      route: 'onboarding',
      urnenWahlbezirke: undefined,
      briefWahlbezirke: undefined
    }
  },
  created () {
    fetch('/urn_districts').then(function (response) {
      if (response.ok) {
        response.json().then(function (uwb) {
          this.urnenWahlbezirke = uwb
        }.bind(this))
      } else {
        throw Error('Something went wrong when fetching the data')
      }
    }.bind(this))
    fetch('/letter_districts').then(function (response) {
      if (response.ok) {
        response.json().then(function (lwb) {
          this.briefWahlbezirke = lwb
        }.bind(this))
      } else {
        throw Error('Something went wrong when fetching the data')
      }
    }.bind(this))
  },
  methods: {
    skipOnboarding () {
      this.route = 'map'
    }
  },
  components: {Onboarding, LeafletMap}
}
</script>

<style>
.github-link-img {
  height: 3em;
}
</style>

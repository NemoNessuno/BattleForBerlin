<template>
  <v-app id="bfb" dark>
    <v-toolbar dark>
      <v-toolbar-title>
        Battle For Berlin
      </v-toolbar-title>
      <v-spacer />
      <v-btn icon @click="resetDiff">
        <v-icon>restore_page</v-icon>
      </v-btn>
      <v-btn @click="route = 'onboarding'" icon v-if="route === 'map'">
        <v-icon>info_outline</v-icon>
      </v-btn>
      <v-btn @click="route = 'map'" icon v-if="route === 'onboarding'">
        <v-icon>map</v-icon>
      </v-btn>
      <v-btn href="https://github.com/NemoNessuno/BattleForBerlin" icon>
        <img src="/static/images/github_logo.png" class="github-link-img" />
      </v-btn>
    </v-toolbar>
    <v-content>
      <onboarding v-if="route === 'onboarding'" @skip="skipOnboarding" />
      <leaflet-map v-if="route === 'map'" />
    </v-content>
    <v-footer v-if="route !== 'map'">
      <span>&copy; 2017, S&ouml;ren Titze, Christian Windolf</span>
    </v-footer>
  </v-app>
</template>

<script>
import Onboarding from './components/Onboarding'
import LeafletMap from './components/LeafletMap'
import {reset} from './backend'
export default {
  name: 'app',
  data () {
    return {
      route: 'onboarding',
      districts: undefined
    }
  },
  methods: {
    skipOnboarding () {
      this.route = 'map'
    },
    resetDiff () {
      reset()
    }
  },
  components: {Onboarding, LeafletMap}
}
</script>

<style lang="sass">
.github-link-img
  height: 1.5em
  width: 1.5em
</style>

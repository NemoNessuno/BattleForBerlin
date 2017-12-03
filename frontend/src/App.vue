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
      <leaflet-map v-if="route === 'map'" :districts="districts || {}" />
    </v-content>
    <v-footer>
      <span>&copy; 2017, S&ouml;ren Titze, Christian Windolf</span>
    </v-footer>
  </v-app>
</template>

<script>
import Onboarding from './components/Onboarding'
import LeafletMap from './components/LeafletMap'
import {fetchDistricts} from './backend'
export default {
  name: 'app',
  data () {
    return {
      route: 'onboarding',
      districts: undefined
    }
  },
  created () {
    fetchDistricts().then(function (districts) {
      this.districts = districts
    }.bind(this)).catch(function () {
      throw new Error('loading of data failed')
    })
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

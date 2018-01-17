<template>
  <v-app id="bfb" dark>
    <v-toolbar dark>
      <v-toolbar-title>
        Battle For Berlin
      </v-toolbar-title>
      <v-spacer />
      <v-btn icon @click="reset" :disabled="diffCount === 0">
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
      <!--
      <onboarding v-if="route === 'onboarding'" @skip="skipOnboarding" />
      -->
      <leaflet-map :style="{height: mapHeight}" class="supermap" />
      <welcome v-if="route === 'welcome'"></welcome>
      <gerry-mander v-if="route === 'gerrymander'" />
    </v-content>
    <v-footer v-if="route !== 'map'">
      <span>&copy; 2017, S&ouml;ren Titze, Christian Windolf</span>
    </v-footer>
  </v-app>
</template>

<script>
import Onboarding from './components/Onboarding'
import LeafletMap from './components/LeafletMap'
import GerryMander from './components/GerryMander'
import Welcome from './components/Welcome'
import {mapState, mapActions, mapGetters} from 'vuex'
export default {
  name: 'app',
  computed: {
    mapHeight () {
      if (this.route === 'map') {
        return 'calc(100vh - 70px)'
      } else {
        return '0'
      }
    },
    ...mapState(['diffCount', 'gerryManderVisible', 'route']),
    ...mapGetters(['currentCounty'])
  },
  mounted () {
    this.loadDistricts()
    this.loadCounties()
    this.loadDiffCount()
  },
  methods: {
    skipOnboarding () {
      this.route = 'map'
    },
    ...mapActions(['reset', 'loadCounties', 'loadDistricts', 'loadDiffCount'])
  },
  components: {Onboarding, LeafletMap, GerryMander, Welcome}
}
</script>

<style lang="sass">
html
  overflow-y: hidden

.github-link-img
  height: 1.5em
  width: 1.5em

.supermap
  transition: height 0.3s ease

.toolbar.afd, .btn.afd
  background-color: #2B9FDB
.toolbar.gruene, .btn.gruene
  background-color: #4E8935
.toolbar.spd, .btn.spd
  background-color: #DB0E2A
.toolbar.cdu, .btn.cdu
  background-color: #000000
.toolbar.fdp, .btn.fdp
  color: #FB0078
  background-color: #FEE943
.toolbar.die_linke, .btn.die_linke
  background-color: #CC008A

.leaflet-control-layers, .application .leaflet-control-zoom a
  background-color: #444444
  color: white
  form.leaflet-control-layers-scrollbar
    overflow-y: hidden
</style>

<template>
  <v-app id="bfb" dark>
    <v-toolbar dark>
  <v-btn icon flat v-if="icon" to="/map">
    <v-icon>{{icon}}</v-icon>
  </v-btn>
  <v-toolbar-title>
    {{title}}
  </v-toolbar-title>
  <v-spacer />
  <v-btn icon @click="reset" :disabled="diffCount === 0 || disabled">
    <v-icon>restore_page</v-icon>
  </v-btn>
  <v-btn to="/info" icon v-if="$route.name === 'map'">
    <v-icon>info</v-icon>
  </v-btn>
  <v-btn to="/map" icon v-if="$route.name === 'info'" >
    <v-icon>map</v-icon>
  </v-btn>
  <v-btn href="https://github.com/NemoNessuno/BattleForBerlin" icon>
    <img src="/static/images/github_logo.png" class="github-link-img" />
  </v-btn>
    </v-toolbar>
    <v-content>
      <transition mode="out-in">
        <router-view></router-view>
      </transition>
    </v-content>
    <v-footer v-if="!$route.meta.footerInvisible">
      <span>&copy; 2017, S&ouml;ren Titze, Christian Windolf</span>
    </v-footer>
  </v-app>
</template>

<script>
import {mapState, mapActions} from 'vuex'
import {BWK_NAMES} from './helpers'
export default {
  name: 'app',
  computed: {
    ...mapState(['diffCount', 'gStatus']),
    title () {
      if (this.$route.name === 'gerrymander') {
        const identifier = this.$route.params.identifier
        return 'Bezirk ' + identifier + ' - ' + BWK_NAMES[identifier]
      }
      if (this.$route.name === 'animation') {
        return this.$route.meta.title + ' ' + this.gStatus
      }
      return this.$route.meta.title
    },
    icon () {
      return this.$route.meta.icon
    },
    disabled () {
      return this.$route.name === 'animation'
    }
  },
  methods: {
    skipOnboarding () {
      this.route = 'map'
    },
    ...mapActions(['reset', 'loadCounties', 'loadDistricts', 'loadDiffCount'])
  }
}
</script>

<style lang="sass">
html
  overflow-y: auto

.github-link-img
  height: 1.5em
  width: 1.5em

.supermap
  transition: height 0.3s ease

.toolbar.afd, .btn.afd, .afd
  background-color: #2B9FDB
.toolbar.gruene, .btn.gruene, .gruene
  background-color: #4E8935
.toolbar.spd, .btn.spd, .spd
  background-color: #DB0E2A
.toolbar.cdu, .btn.cdu, .cdu
  background-color: #000000
.toolbar.fdp, .btn.fdp, .fdp
  color: #FB0078
  background-color: #FEE943
.toolbar.die_linke, .btn.die_linke, .die_linke
  background-color: #CC008A

.leaflet-control-layers, .application .leaflet-control-zoom a
  background-color: #444444
  color: white
  form.leaflet-control-layers-scrollbar
    overflow-y: hidden

.v-enter-active, .v-leave-active
  transition: transform 0.3s ease
.v-leave
  transform: translateY(0)
.v-leave-to
  transform: translateY(100vh)
.v-enter
  transform: scale(0.3)
.v-enter-to
  transform: scale(1)
</style>

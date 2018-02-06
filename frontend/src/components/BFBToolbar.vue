<template>
<v-toolbar dark>
  <v-btn icon flat v-if="icon" href="/map">
    <v-icon>{{icon}}</v-icon>
  </v-btn>
  <v-toolbar-title>
    {{title}}
  </v-toolbar-title>
  <v-btn icon @click="reset" :disabled="diffCount === 0 && disabled">
    <v-icon>restore_page</v-icon>
  </v-btn>
  <v-btn href="/info" icon v-if="$route.name === 'map'">
    <v-icon>info</v-icon>
  </v-btn>
  <v-btn href="/map" icon v-if="$route.name === 'info'" >
    <v-icon>map</v-icon>
  </v-btn>
  <v-btn href="https://github.com/NemoNessuno/BattleForBerlin" icon>
    <img src="/static/images/github_logo.png" class="github-link-img" />
  </v-btn>
</v-toolbar>
</template>

<script>
  import {mapState, mapActions} from 'vuex'
  export default {
    name: 'v-toolbar',
    methods: {
      ...mapActions(['reset'])
    },
    computed: {
      ...mapState(['diffCount']),
    }
  }
</script>

<style scoped>

</style>
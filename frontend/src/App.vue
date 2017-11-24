<template>
  <v-app id="bfb" dark>
    <v-toolbar app fixed clipped-left>
      <v-toolbar-title>
        Battle For Berlin
      </v-toolbar-title>
      <v-spacer />
      <v-toolbar-items class="hidden-sm-and-down">
        <v-btn href="https://github.com/NemoNessuno/BattleForBerlin" flat>
          <img src="/static/images/github_logo.png" class="github-link-img" />
        </v-btn>
      </v-toolbar-items>
    </v-toolbar>
    <v-content>
    </v-content>
    <v-footer>
      <span>&copy; 2017, S&ouml;ren Titze, Christian Windolf</span>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  name: 'app'
}
</script>

<style>
@import 'vuetify/dist/vuetify.min.css'
</style>

<style>
.github-link-img {
  height: 3em;
}
</style>
<template>
  <div>
    <v-toolbar class="primary">
      <v-btn icon to="/map">
        <v-icon>
          close
        </v-icon>
      </v-btn>
      <v-toolbar-title>
        GerryMandering
      </v-toolbar-title>
    </v-toolbar>
    <v-container grid-list-md>
      <v-layout row wrap>
        <v-flex md3>
          <v-list class="accent">
            <v-list-tile>
              <v-list-content class="subheading black--text">
                Was ist Gerrymandering?
              </v-list-content>
            </v-list-tile>
            <v-divider />
            <v-list-tile>
              <v-list-content class="subheading black--text">
                Warum interessiert mich das?
              </v-list-content>
            </v-list-tile>
            <v-divider />
            <v-list-tile>
              <v-list-content class="subheading black--text">
                Was kann man damit machen?
              </v-list-content>
            </v-list-tile>
          </v-list>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
  import OnboardingCard from './OnboardingCard'
  import {mapMutations} from 'vuex'
  export default {
    name: 'onboarding',
    data () {
      return {
        step: 1
      }
    },
    methods: {
      ...mapMutations(['goToMap'])
    },
    components: {OnboardingCard}
  }
</script>

<style scoped>

</style>

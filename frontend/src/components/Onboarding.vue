<template>
  <v-container grid-list-md>
    <v-layout row>
      <v-flex xs12 sm12 md8 offset-md2 lg6 offset-lg3 xl6 offset-xl3>
        <v-stepper v-model="step">
          <v-stepper-header>
            <v-stepper-step step="1" :complete="step > 1">
              Was ist Gerrymandering?
            </v-stepper-step>
            <v-stepper-step step="2" :complete="step > 2">
              Was kann man in Deutschland damit machen?
            </v-stepper-step>
            <v-stepper-step step="3" :complete="step > 3">
              Wieso interessiert mich das?
            </v-stepper-step>
          </v-stepper-header>
          <v-stepper-items>
            <v-stepper-content step="1">
              <onboarding-card
                title="Was ist Gerrymandering?"
                :first="true"
                @next="next"
                @skip="skip">
                Lorem ipsum
              </onboarding-card>
            </v-stepper-content>
            <v-stepper-content step="2">
              <onboarding-card
                title="Was kann man damit machen?"
                @next="next"
                @skip="skip"
                @previous="previous">
                Lorem ipsum
              </onboarding-card>
            </v-stepper-content>
            <v-stepper-content step="3">
              <onboarding-card
                title="Wieso interessiert mich das?"
                :last="true"
                @skip="skip"
                @previous="previous">
                foo - bar = Hello World
              </onboarding-card>
            </v-stepper-content>
          </v-stepper-items>
        </v-stepper>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
  import OnboardingCard from './OnboardingCard'
  export default {
    name: 'onboarding',
    data () {
      return {
        step: 1
      }
    },
    methods: {
      next () {
        this.step += 1
      },
      previous () {
        this.step -= 1
      },
      skip () {
        this.$emit('skip')
      }
    },
    components: {OnboardingCard}
  }
</script>

<style scoped>

</style>
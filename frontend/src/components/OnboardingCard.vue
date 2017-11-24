<template>
  <v-card class="mb-6">
    <v-card-title primary-title>
      <h3 class="headline mb-0">
        {{ title }}
      </h3>
    </v-card-title>
    <v-card-text>
      <slot></slot>
    </v-card-text>
    <v-card-actions>
      <v-btn @click.native="skip">&Uuml;berspringen</v-btn>
      <v-spacer />
      <v-btn v-if="!first" @click.native="previous">Zur&uuml;ck</v-btn>
      <v-btn @click.native="next" v-if="!last">Weiter</v-btn>
      <v-btn @click.native="skip" v-else>Fertig</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
  export default {
    name: 'onboarding-card',
    props: {
      title: {required: true, type: String},
      first: {default: false, type: Boolean},
      last: {default: false, type: Boolean}
    },
    methods: {
      next () {
        this.$emit('next')
      },
      previous () {
        this.$emit('previous')
      },
      skip () {
        this.$emit('skip')
      }
    }
  }
</script>

<style scoped>

</style>
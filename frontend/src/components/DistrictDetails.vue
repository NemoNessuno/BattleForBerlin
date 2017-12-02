<template>
  <div id="sidebar" class="detail-wrapper">
    <v-card  elevation-24>
      <v-card-title>
        <h3 class="headline">{{bezirk}} </h3>
        <h4 class="subheading"> Bezirkswahlkreis {{bwk}} </h4>
      </v-card-title>
      <v-card-text>

      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn @click.native="close">Close</v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
  export default {
    name: 'DistrictDetails',
    props: {
      district: {type: Object, required: true}
    },
    computed: {
      bwk () { return this.district.bwk },
      bezirk () { return this.district.bezname }
    },
    methods: {
      close () {
        this.$emit('close')
      }
    }
  }
</script>

<style scoped>
h3.headline, h4.subheading {
  width: 100%
}
.detail-wrapper {
  padding: 1em;
  position: absolute;
  left: 1em;
  top: 10em;
  width: 30em;
  z-index: 1000;
}
</style>

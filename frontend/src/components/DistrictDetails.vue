<template>
  <div id="sidebar" class="detail-wrapper">
    <v-card  elevation-24>
      <v-card-title>
        <h3 class="headline">Wahlbezirk {{uwbId}}</h3>
      </v-card-title>
      <v-card-text>
        In diesem Wahlbezirk sind ist die Pizza besonders {{pizzaQuality}}
      </v-card-text>
      <v-card-text>
        Ergebnisse:
        {{properties.result}}
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn @click="$emit('close')">Close</v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
  export default {
    name: 'DistrictDetails',
    props: {
      uwbId: {type: Number, required: true},
      properties: {type: Object, required: true}
    },
    computed: {
      pizzaQuality () {
        if (this.uwbId % 2 === 0) {
          return 'gut'
        }
        return 'schlecht'
      }
    }
  }
</script>

<style scoped>
.detail-wrapper {
  padding: 1em;
  position: absolute;
  left: 1em;
  top: 10em;
  width: 30em;
  z-index: 1000;
}
</style>

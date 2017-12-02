<template>
  <div id="sidebar" class="detail-wrapper">
    <v-card  class="elevation-12">
      <v-card-title>
        <h3 class="headline">{{bezirk}} </h3>
        <h4 class="subheading"> Bezirkswahlkreis {{bwk}} </h4>
        <h4 class="subheading"> Wahlbezirk {{districtId}} </h4>
      </v-card-title>
      <v-card-text>
        <v-data-table
          :headers="headers"
          :items="results"
          hide-actions>
          <template slot="items" slot-scope="props">
            <td> {{props.item.name}}</td>
            <td> {{props.item.result}}</td>
          </template>
        </v-data-table>
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
    data () {
      return {
        headers: [
          {text: 'Partei', align: 'left', value: 'name'},
          {text: 'Stimmen', align: 'right', value: 'result'}
        ]
      }
    },
    computed: {
      bwk () { return this.district.bwk },
      bezirk () { return this.district.bezname },
      districtId () { return this.district.identifier},
      results () {
        return [
          {name: 'CDU', value: false, result: this.district.result.cdu},
          {name: 'SPD', value: false, result: this.district.result.spd},
          {name: 'Die Grünen', value: false, result: this.district.result.gruene},
          {name: 'AFD', value: false, result: this.district.result.afd},
          {name: 'FDP', value: false, result: this.district.result.fdp},
          {name: 'Die Linke', value: false, result: this.district.result.die_linke}
        ]
      }
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

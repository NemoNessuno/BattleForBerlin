<template>
  <v-select
    :items="items"
    label="Wahlbezirk"
    v-model="value"
    >
  </v-select>
</template>

<script>
import {changeDistrict} from '@/backend'
export default {
  name: 'select-bwk',
  props: {bwk: {type: String, required: true}, identifier: {type: String, required: true}},
  data () {
    return {
      value: this.bwk,
      items: [
        {text: '075 - Mitte', value: '075'},
        {text: '076 - Pankow', value: '076'},
        {text: '077 - Reinickendorf', value: '077'},
        {text: '078 - Spandau/Charlottenburg-Nord', value: '078'},
        {text: '079 - Steglitz/Zehlendorf', value: '079'},
        {text: '080 - Charlottenburg/Wilmersdorf', value: '080'},
        {text: '081 - Tempelhof/Schöneberg', value: '081'},
        {text: '082 - Neukölln', value: '082'},
        {text: '083 - Friedrichshain/Kreuzb./Prenzlb-Ost', value: '083'},
        {text: '084 - Treptow/Köpenick', value: '084'},
        {text: '085 - Marzahn/Hellersdorf', value: '085'},
        {text: '086 - Lichtenberg', value: '086'}
      ]
    }
  },
  watch: {
    value (newVal) {
      changeDistrict(this.identifier, newVal).then(console.log)
    }
  }
}
</script>

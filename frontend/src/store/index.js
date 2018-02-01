import {COUNTY_KEYS} from './constants'
import actions from './actions'
import getters from './getters'
import mutations from './mutations'

const state = {
  countyProps: undefined,
  districts: undefined,
  districtProps: undefined,
  diffCount: 0,
  diffs: [],
  selectedDistrict: undefined,
  selectedCounty: undefined,
  gerryManderVisible: false,
  route: 'welcome',
  gerrymanderAnimation: undefined,
  districtHash: undefined,
  gActive: false,
  gSteps: undefined,
  gIndex: -1
}

COUNTY_KEYS.forEach(function (key) {
  state[key] = undefined
})

export default {
  state,
  actions,
  getters,
  mutations
}

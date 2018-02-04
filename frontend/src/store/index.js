import {COUNTY_KEYS} from './constants'
import actions from './actions'
import getters from './getters'
import mutations from './mutations'

const state = {
  countyProps: undefined,
  districts: undefined,
  districtProps: undefined,
  districtHash: undefined,
  diffCount: 0,
  diffs: [],
  selectedDistrict: undefined,
  selectedCounty: undefined,
  gerryManderVisible: false,
  route: 'welcome',
  gerrymanderAnimation: undefined,
  gActive: false,
  gSteps: undefined,
  gIndex: -1,
  gStatus: undefined
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

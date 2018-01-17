import actions from './actions'
import getters from './getters'
import mutations from './mutations'

const state = {
  counties: undefined,
  countyProps: undefined,
  districts: undefined,
  districtProps: undefined,
  diffCount: 0,
  diffs: [],
  selectedDistrict: undefined,
  selectedCounty: undefined,
  gerryManderVisible: false,
  route: 'welcome'
}

export default {
  state,
  actions,
  getters,
  mutations
}

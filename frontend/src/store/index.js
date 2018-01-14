import actions from './actions'
import getters from './getters'
import mutations from './mutations'

const state = {
  counties: undefined,
  countyPropes: undefined,
  districts: undefined,
  districtProps: undefined,
  diffCount: 0,
  diffs: [],
  selectedDistrict: undefined,
  selectedCounty: undefined
}

export default {
  state,
  actions,
  getters,
  mutations
}

export default {
  currentDistrict (state) {
    if (!state.districtProps) {
      return undefined
    }
    return state.districtProps[state.selectedDistrict]
  },
  currentCounty (state) {
    if (!state.countyProps) {
      return undefined
    }
    return state.countyProps[state.selectedCounty]
  }
}

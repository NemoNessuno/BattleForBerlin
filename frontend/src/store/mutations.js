export default {
  setDistricts (state, districts) {
    state.districts = districts
    state.districtProps = {}
    districts.forEach(function (district) {
      state.districtProps[district.properties.identifier] = district.properties
    })
  },
  setCounties (state, counties) {
    state.counties = counties
    state.countyProps = {}
    counties.forEach(function (county) {
      state.countyProps[county.properties.bwk] = county.properties
    })
  },
  setDiffCount (state, count) {
    state.diffCount = count
  },
  addDiff (state, diff) {
    state.diff = state.diff.concat([diff])
    state.diffCount = state.diff.length
  },
  selectDistrict (state, identifier) {
    state.selectedCounty = undefined
    state.selectedDistrict = identifier
  },
  selectCounty (state, identifier) {
    state.selectedCounty = identifier
    state.selectedDistrict = undefined
  },
  unselectItem (state) {
    state.selectedCounty = undefined
    state.selectedDistrict = undefined
  }
}

export default {
  setDistricts (state, districts) {
    state.districts = districts
    state.districtProps = {}
    state.districtHash = {}
    districts.forEach(function (district) {
      state.districtProps[district.properties.identifier] = {...district.properties}
      state.districtHash[district.identifier] = {...district}
    })
  },
  setCounties (state, counties) {
    if (!state.countyProps) {
      state.countyProps = {}
    }
    counties.forEach(function (county) {
      const bwk = county.properties.bwk
      state.countyProps[bwk] = county.properties
      state['county_' + bwk] = county
    })
  },
  setDiffCount (state, count) {
    state.diffCount = count
  },
  addDiff (state, diff) {
    state.diffs = state.diffs.concat([diff])
    state.diffCount = state.diffs.length
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
  },
  setGerryManderVisible (state, visible) {
    state.gerryManderVisible = visible
  },
  goToMap (state) {
    state.route = 'map'
  },
  goToGerryMander (state) {
    state.route = 'gerrymander'
  },
  goToAbout (state) {
    state.route = 'about'
  },
  setGerrymanderAnimation (state, gerrymanderAnimation) {
    state.gerrymanderAnimation = gerrymanderAnimation
  }
}

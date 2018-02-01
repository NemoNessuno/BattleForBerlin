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
  },
  gComplete (state) {
    if (!state.gSteps) {
      return false
    }
    return state.gSteps[state.gSteps.length - 1].action === 'stop'
  },
  currentGStep (state) {
    if (!state.gSteps) {
      return undefined
    }
    return state.gSteps[state.gStepsIndex]
  }
}

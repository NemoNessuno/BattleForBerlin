import {COUNTY_KEYS} from './constants'

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
  counties (state) {
    const result = {}
    for (let key of COUNTY_KEYS) {
      result[key] = state[key]
    }
    return result
  }
}

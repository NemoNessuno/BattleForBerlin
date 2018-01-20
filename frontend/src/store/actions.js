import {Observable} from 'rxjs/Observable'
import 'rxjs/add/observable/of'
import 'rxjs/add/observable/timer'
import 'rxjs/add/operator/concat'
import 'rxjs/add/operator/mapTo'

export default {
  loadCounties ({commit}) {
    return fetch('/api/counties').then(resp => resp.json())
      .then(counties => {
        commit('setCounties', counties)
        return counties
      })
  },
  loadDistricts ({commit}) {
    return fetch('/api/districts/merged_diff').then(resp => resp.json())
      .then(districts => {
        commit('setDistricts', districts)
        return districts
      })
  },
  loadDiffCount ({commit}) {
    return fetch('/api/diff/count').then(resp => resp.json())
      .then(({count}) => {
        commit('setDiffCount', count)
        return count
      })
  },
  reset ({commit, dispatch}) {
    const body = ''
    const headers = new Headers({
      'Accept': 'application/json'
    })
    return fetch('/api/diff/reset', {method: 'post', body, headers}).then(resp => resp.json())
      .then(resp => {
        commit('setDiffCount', 0)
        dispatch('loadCounties')
        return resp
      })
  },
  changeDistrict ({commit, dispatch}, {identifier, bwk}) {
    const body = JSON.stringify({identifier, bwk})
    const headers = new Headers({
      'Content-Type': 'application/json',
      'Accept': 'application/json, text/plain, */*'
    })
    return fetch('/api/diff/create', {method: 'post', body, headers})
      .then(resp => resp.json())
      .then(resp => {
        commit('addDiff', {identifier, bwk})
        dispatch('loadCounties')
        return resp
      })
  },
  async gerryMander ({commit, dispatch}, {bwk, party, withReset}) {
    if (withReset) {
      commit('setAlgorithmProgress', {shifts: 0, totalShifts: 0, reset: false})
      await dispatch('reset')
    }
    commit('setAlgorithmProgress', {shifts: 0, totalShifts: 0, reset: true})
    const body = JSON.stringify({bwk, party})
    const headers = new Headers({
      'Content-Type': 'application/json',
      'Accept': 'application/json, text/plain, */*'
    })
    const resp = await fetch('/api/gerrymander', {method: 'post', body, headers})
    let data = await resp.json()
    data = data.map(function (value, index) { return {value, index} })
    commit('setAlgorithmProgress', {shfits: 0, totalShifts: data.length, reset: true})
    const delayedRenderer = data.reduce(function (obs, value) {
      if (value.index === 0) {
        return obs.concat(Observable.of(value))
      }
      return obs.concat(Observable.timer(500).mapTo(value))
    }, Observable.timer(1000))
    delayedRenderer.subscribe(
      function (item) {
        if (typeof item === 'number') {
          commit('setAlgorithmProgress', {shifts: 0, totalShifts: data.length, reset: true})
          return
        }
        commit('setCounties', item.value)
        const shifts = item.index + 1
        commit('setAlgorithmProgress', {shifts, totalShifts: data.length, reset: true})
      },
      console.error,
      function () {
        Observable.timer(4000).subscribe(function () {
          commit('setAlgorithmProgress', undefined)
        })
      }
    )
  }
}

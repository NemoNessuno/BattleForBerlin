import {retryPromise} from '@/helpers'

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
  async gerrymander ({commit, dispatch}, {bwk, party, withReset}) {
    const body = JSON.stringify({bwk, party})
    const headers = new Headers({
      'Content-Type': 'application/json',
      'Accept': 'application/json, text/plain, */*'
    })
    await retryPromise(() => fetch('/api/gsteps').then(resp => {
      if (resp.status === 200) {
        throw new Error('there are still gerrymander steps available')
      }
    }), 2000)
    const resp = await fetch('/api/gerrymander', {method: 'post', body, headers}).catch(() => {
      fetch('/a[i/gsteps').then()
    })
    let data = await resp.json()
    return data
  }
}

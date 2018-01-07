import { BehaviorSubject } from 'rxjs/BehaviorSubject'

export function reset () {
  const body = ''
  const headers = new Headers({
    'Accept': 'application/json'
  })
  return fetch('/api/diff/reset', {method: 'post', body, headers})
}

export class DistrictStore {
  _districts = undefined
  _districts$ = new BehaviorSubject([])
  _fetchingDistricts = false

  _counties = undefined
  _counties$ = new BehaviorSubject([])
  _fetchingCounties = false

  init () {
    this._fetchDistricts()
    this._fetchCounties()
  }

  get districts () {
    if (!this._districts && !this._fetchingDistricts) {
      this._fetchingDistricts()
    }
    return this._districts$.asObservable()
  }

  _fetchDistricts () {
    this._fetchingDistricts = true
    fetch('/api/districts/merged_diff').then(resp => resp.json())
      .then(districts => {
        this._fetchingDistricts = false
        this._districts = districts
        this._districts$.next(districts)
      })
  }

  get counties () {
    if (!this._counties && !this._fetchingCounties) {
    }
    return this._counties$.asObservable()
  }

  _fetchCounties () {
    this._fetchingCounties = true
    fetch('/api/counties').then(resp => resp.json())
      .then(districts => {
        this._counties = districts
        this._counties$.next(districts)
      })
  }

  changeDistrict (districtId, bwk) {
    const body = JSON.stringify({identifier: districtId, bwk})
    const headers = new Headers({
      'Content-Type': 'application/json',
      'Accept': 'application/json, text/plain, */*'
    })
    return fetch('/api/diff/create', {method: 'post', body, headers})
      .then(resp => {
        this._fetchCounties()
        return resp
      })
  }
}

export const store = new DistrictStore()

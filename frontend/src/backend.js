import { BehaviorSubject } from 'rxjs/BehaviorSubject'

export class DistrictStore {
  _districts = undefined
  _districts$ = new BehaviorSubject([])
  _fetchingDistricts = false

  _counties = undefined
  _counties$ = new BehaviorSubject([])
  _fetchingCounties = false

  _diffCount = 0
  _diffCount$ = new BehaviorSubject(0)

  init () {
    this._fetchDistricts()
    this._fetchCounties()
    this._fetchDiffCount()
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
      this._fetchCounties()
    }
    return this._counties$.asObservable()
  }

  _fetchCounties () {
    this._fetchingCounties = true
    fetch('/api/counties').then(resp => resp.json())
      .then(districts => {
        this._fetchingCounties = false
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
        this._diffCount = this._diffCount + 1
        this._diffCount$.next(this._diffCount)
        return resp
      })
  }

  get diffCount () {
    return this._diffCount$.asObservable()
  }

  _fetchDiffCount () {
    fetch('/api/diff/count').then(resp => resp.json())
      .then(({count}) => {
        this._diffCount = count
        this._diffCount$.next(count)
      })
  }

  reset () {
    const body = ''
    const headers = new Headers({
      'Accept': 'application/json'
    })
    return fetch('/api/diff/reset', {method: 'post', body, headers}).then((resp) => {
      this._diffCount = 0
      this._diffCount$.next(0)
      this._fetchCounties()
      return resp
    })
  }
}

export const store = new DistrictStore()

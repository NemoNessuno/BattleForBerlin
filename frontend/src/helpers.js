import {Observable} from 'rxjs/Observable'
import 'rxjs/add/observable/timer'
import 'rxjs/add/observable/forkJoin'
import 'rxjs/add/operator/map'

export function maxProp (obj) {
  let maxKey = ''
  let maxVal = -Infinity
  Object.keys(obj).forEach(key => {
    if (obj[key] > maxVal) {
      maxVal = obj[key]
      maxKey = key
    }
  })
  return maxKey
}

export const PARTY_COLORS = {
  afd: '#2B9FDB',
  gruene: '#4E8935',
  spd: '#DB0E2A',
  cdu: '#000000',
  fdp: '#FEE943',
  die_linke: '#CC008A'
}

export function minAwait (observable, timeout = 500) {
  const timeoutOb = Observable.timer(500)
  return Observable.forkJoin(observable, timeoutOb).map(arr => arr[0])
}

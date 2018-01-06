export function fetchDistricts () {
  const merged = fetch('/api/districts/merged').then(resp => resp.json())
  const counties = fetch('/api/counties').then(resp => resp.json())
  return Promise.all([merged, counties]).then(function (districts) {
    const [merged, counties] = districts
    return {merged, counties}
  })
}

export function changeDistrict (districtId, bwk) {
  const body = JSON.stringify({identifier: districtId, bwk})
  const headers = new Headers({
    'Content-Type': 'application/json',
    'Accept': 'application/json, text/plain, */*'
  })
  return fetch('/api/diff/create', {method: 'post', body, headers})
}

export function reset () {
  const body = ''
  const headers = new Headers({
    'Accept': 'application/json'
  })
  return fetch('/api/diff/reset', {method: 'post', body, headers})
}

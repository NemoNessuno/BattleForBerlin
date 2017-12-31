export function fetchDistricts () {
  const merged = fetch('/api/districts/merged').then(resp => resp.json())
  const counties = fetch('/api/counties').then(resp => resp.json())
  return Promise.all([merged, counties]).then(function (districts) {
    const [merged, counties] = districts
    return {merged, counties}
  })
}

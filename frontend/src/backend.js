export function fetchDistricts () {
  const ballotBox = fetch('/api/districts/ballot').then(resp => resp.json())
  const letters = fetch('/api/districts/letters').then(resp => resp.json())
  const counties = fetch('/api/counties').then(resp => resp.json())
  return Promise.all([ballotBox, letters, counties]).then(function (districts) {
    const [ballot, letters, counties] = districts
    return {ballot, letters, counties}
  })
}

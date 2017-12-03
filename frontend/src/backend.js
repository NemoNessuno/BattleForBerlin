export function fetchDistricts () {
  const ballotBox = fetch('/api/districts/ballot').then(resp => resp.json())
  const letters = fetch('/api/districts/letters').then(resp => resp.json())
  return Promise.all([ballotBox, letters]).then(function (districts) {
    const [ballot, letters] = districts
    return {ballot, letters}
  })
}

export function fetchDistricts () {
  const ballotBox = fetch('/api/districts/ballot').then(resp => resp.json())
  const letters = fetch('/api/districts/letters').then(resp => resp.json())
  const counties = fetch('/api/counties').then(resp => resp.json())
    .then(function (results) {
      return results.map(function (item) {
        let {properties} = item
        const result = {}
        Object.keys(properties.l_result).forEach((key) => {
          result[key] = properties.l_result[key] + properties.u_result[key]
        })
        properties = {...properties, result}
        return {...item, properties}
      })
    })
  return Promise.all([ballotBox, letters, counties]).then(function (districts) {
    const [ballot, letters, counties] = districts
    return {ballot, letters, counties}
  })
}

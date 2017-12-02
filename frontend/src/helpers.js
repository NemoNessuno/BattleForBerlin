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
  die_linke: '#D8101F'
}

export function maxProp(obj) {
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
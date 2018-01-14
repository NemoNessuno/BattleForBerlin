import {BWK_NAMES} from '@/helpers'

export default {
  computed: {
    bezirk () {
      let bwk
      if (this.district) {
        bwk = this.district.bwk
      } else {
        bwk = this.bwk
      }
      return BWK_NAMES[bwk]
    }
  }
}

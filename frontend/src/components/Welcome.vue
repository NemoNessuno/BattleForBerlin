<template>
  <div>
    <svg height="500" width="500" >
      <svg x="200" >
        <path class="fu-green show first" d="M290 10 H 22 Q 10 10 10 22 V290 H278 Q 290 290 290 278  Z"  />
      </svg>
      <svg x="100" y="100">
        <path class="fu-lightblue show second" d="M290 10 H 22 Q 10 10 10 22 V290 H278 Q 290 290 290 278  Z"  />
      </svg>
      <svg y="200">
        <path class="fu-darkblue show third" d="M290 10 H 22 Q 10 10 10 22 V290 H278 Q 290 290 290 278  Z"  />
      </svg>
    </svg>
  </div>
</template>

<script>
  export default {
    name: 'welcome'
  }
</script>

<style lang="sass" scoped>
@keyframes fadein
  from
    opacity: 0
  to
    opacity: 1
div
  background-color: white
  width: 100%
  padding: 1em
svg
  display: block
  margin: auto
  stroke-width: 20px
path
  fill: none
  &.fu-green
    stroke: #99CC00
  &.fu-lightblue
    stroke: #0066CC
  &.fu-darkblue
    stroke: #003366
.show
  animation-name: fadein
  animation-duration: 0.5s
  animation-timing-function: ease
  animation-fill-mode: backwards
  &.first
    animation-delay: 0
  &.second
    animation-delay: 0.5s
  &.third
    animation-delay: 1s


</style>
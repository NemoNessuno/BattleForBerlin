<template>
  <div class="welcome-wrapper">
    <div class="svg-wrapper">
      <svg viewBox="0 0 500 500" >
        <svg x="200">
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
    <div class="title-wrapper">
      <h1 class="display-3 fu-darkblue show bfb" >
        Battle For Berlin
      </h1>
      <h1 class="display-2 fu-lightblue show bfb">
        A Gerrymandering Tool
      </h1>
      <div class="button-wrapper" >
        <v-btn raised class="blue elevation-4 welcome-button" to="/map" large >
          Start
        </v-btn>
        <v-btn raised light large class="elevation-4 welcome-button" to="/info">
          Gerrymandering?
          <v-icon right>info</v-icon>
        </v-btn>
      </div>
    </div>
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

@keyframes flyin
  from
    transform: translateX(70vw)
  to
    transform: translateX(0)

div.welcome-wrapper
  background-color: white
  width: 100%
  display: flex
  padding: 1em
  height: calc(100vh - 100px)
div.title-wrapper
  padding-top: 50px
div.svg-wrapper
  text-align: center
  width: 40%
svg
  height: 320px
  width: 320px
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
  animation-timing-function: ease
  animation-fill-mode: backwards
  &.bfb
    animation-duration: 2s
  &.first
    animation-duration: 0.3s
    animation-delay: 0.1s
  &.second
    animation-duration: 0.3s
    animation-delay: 0.5s
  &.third
    animation-delay: 0.9s
    animation-duration: 0.3s

h1.fu-lightblue
  color: #0066CC
h1.fu-darkblue
  color: #003366

.welcome-button
  width: 14em

.button-wrapper
  animation: flyin 0.3s 1s
  animation-timing-function: ease
  animation-fill-mode: backwards
  text-align: center
  margin-top: 2em
</style>
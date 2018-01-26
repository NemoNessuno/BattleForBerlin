import VueRouter from 'vue-router'

import LeafletMap from './components/LeafletMap'
import GerryMander from './components/GerryMander'
import Onboarding from './components/Onboarding'
import Welcome from './components/Welcome'
import AnimationMap from './components/AnimationMap'

const routes = [
  {path: '/map/:identifier?', component: LeafletMap},
  {path: '/votingdistrict/:identifier', component: GerryMander},
  {path: '/info', component: Onboarding},
  {path: '/animation', component: AnimationMap},
  {path: '/', component: Welcome}
]

export default new VueRouter({routes})

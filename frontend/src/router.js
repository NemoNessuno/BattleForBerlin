import VueRouter from 'vue-router'

import LeafletMap from './components/LeafletMap'
import GerryMandering from './components/GerryMandering'
import Onboarding from './components/Oboarding'
import Welcome from './components/Welcome'

const routes = [
  {path: '/map/:identifier?', component: LeafletMap},
  {path: '/votingdistrict/:indentifier', component: GerryMandering},
  {path: '/info', component: Onboarding},
  {path: '/', component: Welcome}
]

export default new VueRouter({routes})

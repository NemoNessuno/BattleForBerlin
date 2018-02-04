import VueRouter from 'vue-router'

import LeafletMap from './components/LeafletMap'
import GerryMander from './components/GerryMander'
import Onboarding from './components/Onboarding'
import Welcome from './components/Welcome'
import AnimationMap from './components/AnimationMap'

const routes = [
  {
    path: '/map/:identifier?',
    component: LeafletMap,
    name: 'map',
    meta: {
      title: 'Battle For Berlin',
      footerInvisible: true
    }
  },
  {
    path: '/votingdistrict/:identifier',
    component: GerryMander,
    name: 'gerrymander',
    meta: {
      icon: 'arrow_back',
      title: 'bezirk'
    }
  },
  {
    path: '/info',
    component: Onboarding,
    meta: {
      title: 'Gerrymandering Information',
      icon: 'arrow_back'
    }
  },
  {
    path: '/animation',
    component: AnimationMap,
    name: 'animation',
    meta: {
      title: 'GerryMandering',
      icon: 'arrow_back',
      footerInvisible: true
    }
  },
  {
    path: '/',
    component: Welcome,
    name: 'welcome',
    meta: {
      title: 'Battle For Berlin'
    }
  }
]

export default new VueRouter({routes})

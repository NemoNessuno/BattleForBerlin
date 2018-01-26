// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import Vuex from 'vuex'
import storeDefinition from './store'
import Vuetify from 'vuetify'
import VueRouter from 'vue-router'
import App from './App'
import router from './router'

Vue.use(Vuex)
Vue.use(Vuetify)
Vue.use(VueRouter)
Vue.config.productionTip = false

const store = new Vuex.Store(storeDefinition)
store.dispatch('loadDistricts')
store.dispatch('loadCounties')
store.dispatch('loadDiffCount')

/* eslint-disable no-new */
new Vue({
  el: '#app',
  template: '<App/>',
  components: { App },
  store,
  router
})

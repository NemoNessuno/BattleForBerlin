// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import Vuex from 'vuex'
import store from './store'
import Vuetify from 'vuetify'
import VueRouter from 'vue-router'
import App from './App'
import router from './router'

Vue.use(Vuex)
Vue.use(Vuetify)
Vue.use(VueRouter)
Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  template: '<App/>',
  components: { App },
  store: new Vuex.Store(store),
  router
})

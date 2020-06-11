import Vue from 'vue'
import './plugins/axios'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'
import store from './store'

Vue.config.productionTip = false
Vue.config.silent = false
Vue.config.ignoredElements = [
  'vue-emoji-mart-picker'
]

new Vue({
  router,
  vuetify,
  store,
  render: h => h(App)
}).$mount('#app')

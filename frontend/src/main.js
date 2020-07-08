import Vue from 'vue'
import './plugins/axios'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'
import store from './store'
import * as fb from 'firebase/app'

Vue.config.productionTip = false
Vue.config.silent = false
Vue.config.ignoredElements = [
  'vue-emoji-mart-picker'
]

new Vue({
  router,
  vuetify,
  store,
  render: h => h(App),
  created () {
    var firebaseConfig = {
      apiKey: 'AIzaSyCfQOtMhNhq-bhUmn4vgG4j9dsHYv6DWwU',
      authDomain: 'jooster-social-auth.firebaseapp.com',
      databaseURL: 'https://jooster-social-auth.firebaseio.com',
      projectId: 'jooster-social-auth',
      storageBucket: 'jooster-social-auth.appspot.com',
      messagingSenderId: '567687865071',
      appId: '1:567687865071:web:8d6029b540ed5bc812b11a',
      measurementId: 'G-0EVXSPZ084'
    }
    fb.initializeApp(firebaseConfig)
    fb.analytics()
  }
}).$mount('#app')

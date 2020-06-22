import Vue from 'vue'
import Vuetify from 'vuetify/lib'

Vue.use(Vuetify)

export default new Vuetify({
  theme: {
    themes: {
      light: {
        primary: '#2C3138',
        secondary: '#FFFFFF',
        accent: '#F98500',
        error: '#B2221E'
      }
    }
  }
})

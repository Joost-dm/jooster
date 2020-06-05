<template>
  <v-app id="app">
   <div class="scroll-block"></div>
   <template v-if="error">
     <v-snackbar
        :multi-line="true"
        color="error"
        @input="closeError"
        :value="true"
        :timeout="3000"
      >
        {{ error.message }}
        <v-btn
          color="dark"
          text
          @click="closeError"
        >
          Close
        </v-btn>
      </v-snackbar>
  </template>
  <global-loader v-if="globalLoading"></global-loader>
  <navigation v-else></navigation>
  </v-app>
</template>

<script>
import Navigation from './components/Navigation'
import GlobalLoader from './components/loaders/GlobalLoader'

export default {
  name: 'App',
  data: () => ({
  }),
  components: {
    navigation: Navigation,
    'global-loader': GlobalLoader
  },
  methods: {
    closeError () {
      this.$store.dispatch('clearError')
    }
  },
  computed: {
    error () {
      return this.$store.getters.error
    },
    user () {
      return this.$store.getters.getCurrentUser
    },
    loading () {
      return this.$store.getters.loading
    },
    globalLoading () {
      return this.$store.getters.globalLoading
    }
  },
  created () {
    this.$store.dispatch('checkForLocalAuthToken')
  }
}
</script>
<style>
html {
  overflow: hidden !important;
}
#app {
  height: 100vh;
}

/* Размеры скроллбара */
::-webkit-scrollbar {
    width: 5px;
}
/* Трек поле скроллбара */
::-webkit-scrollbar-track {
    -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.3);
    background: white;
}
/* Ползунок скроллбара */
::-webkit-scrollbar-thumb {
    border-radius: 2px ;
    -webkit-box-shadow: inset 0 0 6px black;
    background: grey;
}
</style>

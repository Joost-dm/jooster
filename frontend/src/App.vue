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
  <login v-else-if="!user"></login>
  <navigation v-else></navigation>
  </v-app>
</template>

<script>
import Navigation from './components/Navigation'
import GlobalLoader from './components/loaders/GlobalLoader'
import Login from './views/auth/Login'

export default {
  name: 'App',
  data: () => ({
  }),
  components: {
    navigation: Navigation,
    'global-loader': GlobalLoader,
    login: Login
  },
  methods: {
    closeError () {
      this.$store.dispatch('clearError')
    },
    mobileScreenHeightController () {
      var viewportHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0)
      var appBarHeight = document.getElementById('v-app-bar').offsetHeight
      var headerHeight = document.getElementsByClassName('primary-view__header')[0].offsetHeight
      var bottomFormHeight = document.getElementsByClassName('primary-view__bottom-form')[0].offsetHeight
      var primaryBody = document.getElementsByClassName('primary-view__body')[0]
      primaryBody.style.height = (viewportHeight - appBarHeight - headerHeight - bottomFormHeight + 12) + 'px'
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
  },
  mounted () {
    window.addEventListener('resize', this.mobileScreenHeightController)
  }
}
</script>
<style lang="scss">
@import "styles/variables.scss";

html {
  overflow: hidden !important;
}
body {
  max-height: 50vh;
  .primary-view__main {
    max-height: 100%;
  }
}
/* Размеры скроллбара */
::-webkit-scrollbar {
    width: 5px;
}
/* Трек поле скроллбара */
::-webkit-scrollbar-track {
    -webkit-box-shadow: inset 0 0 3px $third-party;
    background: $secondary;
}
/* Ползунок скроллбара */
::-webkit-scrollbar-thumb {
    border-radius: 2px ;
    background: $primary;
}
</style>

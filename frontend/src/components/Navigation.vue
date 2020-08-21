<template>
  <div>
    <div class="api-info" >
      <api_info></api_info>
    </div>
    <v-navigation-drawer
      id="nav-drawer"
      v-model="primaryDrawer.model"
      :clipped="primaryDrawer.clipped"
      :floating="primaryDrawer.floating"
      :mini-variant="primaryDrawer.mini"
      :permanent="primaryDrawer.type === 'permanent'"
      :temporary="primaryDrawer.type === 'temporary'"
      app
    >
      <branches></branches>
    </v-navigation-drawer>
    <v-app-bar
      id="v-app-bar"
      :clipped-left="primaryDrawer.clipped"
      height="35"
      app>
       <button
         id="hamburger"
         @click.stop="primaryDrawer.model = !primaryDrawer.model"
         @click="hideAPIInfo"
         class="hamburger hamburger--elastic is-active"
         type="button"
         title="Переключить меню навигации">
        <span class="hamburger-box">
          <span class="hamburger-inner"></span>
        </span>
      </button>
      <span v-if="user"> <b>{{user.displayed}}</b></span>
      <v-icon class="app-bar__icon" @click="toggleAccountSettings">mdi-account-cog</v-icon>
      <span class="app-bar__online_counter">online: {{usersOnline.length}}</span> <!-- todo  -->
      <v-spacer></v-spacer>
      <v-icon class="app-bar__icon" @click="toggleAPIInfo">mdi-api</v-icon>
      <v-icon @click="logout" class="app-bar__icon">mdi-logout</v-icon>
    </v-app-bar>
    <account_settings></account_settings>
    <v-content>
      <router-view></router-view>
    </v-content>
  </div>
</template>

<script>
import Branches from './forum/ForumDrawer'
import AccountSettings from './forum/AccountSettings'
import APIInfo from '@/views/forum/APIInfo'

export default {
  components: {
    branches: Branches,
    account_settings: AccountSettings,
    api_info: APIInfo
  },
  name: 'Navigation',
  data: () => ({
    drawers: ['Default (no property)', 'Permanent', 'Temporary'],
    primaryDrawer: {
      model: null,
      type: 'default (no property)',
      clipped: true,
      floating: false,
      mini: false
    }
  }),
  methods: {
    logout () {
      this.$store.dispatch('logoutUser', this.loginData)
    },
    toggleAccountSettings () {
      if (this.accountSettingsIsShown) {
        this.$store.dispatch('setAccountSettingsWindowStatus', false)
      } else {
        this.$store.dispatch('setAccountSettingsWindowStatus', true)
      }
    },
    async onlineChecker () {
      function checker () {
        this.$store.dispatch('getUsersOnline')
      }
      await setInterval(checker.bind(this), 60000)
    },
    hamburgerController () {
      const hamburger = document.getElementById('hamburger')
      if (document.querySelector('nav').style.transform === 'translateX(0%)') {
        hamburger.classList.add('is-active')
      } else {
        hamburger.classList.remove('is-active')
      }
    },
    toggleAPIInfo () {
      const APIInfo = document.getElementsByClassName('api-info')[0]
      if (APIInfo.style.transform === 'translateX(0px)') {
        APIInfo.style.transform = 'translateX(-100%)'
      } else {
        APIInfo.style.transform = 'translateX(0px)'
      }
    },
    hideAPIInfo () {
      const APIInfo = document.getElementsByClassName('api-info')[0]
      if (APIInfo.style.transform === 'translateX(0px)') {
        APIInfo.style.transform = 'translateX(-100%)'
        this.primaryDrawer.model = true
      }
    }
  },
  computed: {
    user () {
      return this.$store.getters.getCurrentUser
    },
    accountSettingsIsShown () {
      return this.$store.getters.accountSettingsIsShown
    },
    usersOnline () {
      return this.$store.getters.getUsersOnline
    }
  },
  updated () {
    this.hamburgerController()
  },
  mounted () {
    this.hamburgerController()
    this.onlineChecker()
  }
}
</script>

<style scoped lang="scss">
@import '../styles/hamburger';
@import '../styles/variables';
#v-app-bar {
  z-index: 10;
  background-color: $app-bar__background-color;
  color: $app-bar__text__font-color;
}

#v-app-bar a {
  text-decoration-line: none;
  color: $app-bar__link__font-color;
}
#v-app-bar a:hover {
  text-decoration-line: none;
  color: $app-bar__link__font-color-hover;
}
.app-bar__icon {
  margin: 0 3px 0 10px;
  color: $secondary;
  cursor: pointer;
}

.app-bar__online_counter {
  margin-left: 10px;
  font-weight: bold;
  font-size: 12px;
  cursor: default;
}
.app-bar__icon:hover {
  color: $extra;
}
#nav-drawer {
  overflow: hidden;
  width: 500px;
}
#hamburger {
  margin-left: -20px;
}

.api-info {
  width: 100vw;
  height: calc(100vh - #{$navigation-app-bar-height});
  position: fixed;
  left: 0;
  top: $navigation-app-bar-height;
  z-index: 7;
  transition: 0.7s;
  transform: translateX(-100%);
  overflow-y: auto;
}

@media screen and (max-width: 595px){
  #nav-drawer {
    padding-top: $navigation-app-bar-height;
  }
}
</style>

<template>
  <div>
    <div class="api-info" >
      <api_info></api_info>
    </div>
    <a href="#api-navigation">
      <div class="api-info__up-button">
        <v-icon class="api-info__up-button-icon">mdi-arrow-up</v-icon>
      </div>
    </a>
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
      <span v-if="user" class="app-bar_username">{{user.displayed}}</span>
      <v-icon class="app-bar__icon" @click="toggleAccountSettings">mdi-account-cog</v-icon>
      <span class="app-bar__online_counter">online: {{usersOnline.length}}</span> <!-- todo  -->
      <v-spacer></v-spacer>
      <v-icon class="app-bar__icon" @click="toggleAPIInfo">mdi-api</v-icon>
      <v-icon @click="logout" class="app-bar__icon">mdi-logout</v-icon>
    </v-app-bar>
    <account_settings></account_settings>
    <v-content class="v-content">
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
      const APIUpButton = document.getElementsByClassName('api-info__up-button')[0]
      if (APIInfo.style.transform === 'translateX(0px)') {
        APIInfo.style.transform = 'translateX(-100%)'
        APIUpButton.style.transform = 'translateY(200%)'
      } else {
        APIInfo.style.transform = 'translateX(0px)'
        APIUpButton.style.transform = 'translateY(-10%)'
      }
    },
    hideAPIInfo () {
      const APIUpButton = document.getElementsByClassName('api-info__up-button')[0]
      const APIInfo = document.getElementsByClassName('api-info')[0]
      if (APIInfo.style.transform === 'translateX(0px)') {
        APIInfo.style.transform = 'translateX(-100%)'
        APIUpButton.style.transform = 'translateY(200%)'
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
.v-content {
  padding-top: 0 !important;
}
.api-info__up-button {
  display: flex;
  position: absolute;
  top: calc(100vh - #{$navigation-app-bar-height} - 40px);
  border-radius: 100%;
  right: 10vw;
  width: 80px;
  height: 80px;
  background-color: $primary;
  opacity: 0.6;
  z-index: 15;
  justify-content: center;
  align-items: center;
  transition: 0.5s;
  transform: translateY(200%);
}
.api-info__up-button:hover {
  opacity: 0.9;
}
.api-info__up-button-icon {
  font-size: 50px;
  color: $hover;
}
#v-app-bar {
  z-index: 10;
  background-color: $app-bar__background-color;
  color: $app-bar__text__font-color;
  position: relative;
}

#v-app-bar a {
  text-decoration-line: none;
  color: $app-bar__link__font-color;
}
#v-app-bar a:hover {
  text-decoration-line: none;
  color: $app-bar__link__font-color-hover;
}
.app-bar_username {
  font-size: 12px;
  font-weight: 400;
}
.app-bar__icon {
  margin: 0 3px 0 10px;
  color: $secondary;
  cursor: pointer;
}
.app-bar__online_counter {
  margin-left: 10px;
  font-weight: 400;
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

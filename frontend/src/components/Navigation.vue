<template>
  <div>
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
         @click="toggleHamburger"
         @click.stop="primaryDrawer.model = !primaryDrawer.model"
         class="hamburger hamburger--elastic is-active"
         type="button"
         title="Переключить меню навигации">
        <span class="hamburger-box">
          <span class="hamburger-inner"></span>
        </span>
      </button>
      <span v-if="user"> <b>{{user.displayed}}</b></span>
          <v-spacer></v-spacer>
          <v-icon class="app-bar__icon">mdi-api</v-icon>
          <v-icon @click="logout" class="app-bar__icon">mdi-logout</v-icon>
    </v-app-bar>
    <v-content>
      <router-view></router-view>
    </v-content>
  </div>
</template>

<script>
import Branches from './forum/ForumDrawer'
export default {
  components: {
    branches: Branches
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
    toggleHamburger () {
      document.getElementById('hamburger').classList.toggle('is-active')
    }
  },
  computed: {
    user () {
      return this.$store.getters.getCurrentUser
    }
  },
  mounted () {
    if (document.documentElement.clientWidth < 595) {
      document.getElementById('hamburger').classList.toggle('is-active')
    }
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
  margin-left: 15px;
  color: $secondary;
  cursor: pointer;
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
@media screen and (max-width: 595px){
  #nav-drawer {
    padding-top: $navigation-app-bar-height;
  }
}
</style>

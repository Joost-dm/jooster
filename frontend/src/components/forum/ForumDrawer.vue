<template>
  <v-container fluid class="pa-0">
    <div class="forum-drawer__main">
      <div class="forum-drawer__header"></div>
      <div class="forum-drawer__body" >
        <v-list color="error" class="pa-0 drawer-menu">
          <v-list-group class="drawer-menu__group" >
            <template v-slot:activator>
              <v-list-item-icon><v-icon>mdi-file-tree-outline</v-icon></v-list-item-icon>
              <v-list-item-title>Навигация</v-list-item-title>
            </template>
            <router-link
              active-class="drawer-menu__branch-link__active"
              class="drawer-menu__item"
              v-for="(link, i) in navigationLinks"
              :to="link.link"
              :key="i">
              <v-list-item link>
                <v-list-item-icon><v-icon>{{link.icon}}</v-icon></v-list-item-icon>
                <v-list-item-title @click="toggleHamburger">{{link.title}}</v-list-item-title>
              </v-list-item>
            </router-link>
          </v-list-group>
          <v-list-group value="true" class="drawer-menu__group">
            <template v-slot:activator>
              <v-list-item-icon><v-icon>mdi-form-select</v-icon></v-list-item-icon>
              <v-list-item-title>Разделы</v-list-item-title>
            </template>
            <div v-for="branch in currentForumBranches"  :key="branch.id" class="drawer-menu__branch-link">
              <router-link active-class="drawer-menu__branch-link__active"
                :to="{ name: 'Forum', params: { forumId: currentForum.id, branchId: branch.id }}">
              <div @click="setBranchInPrimary(true)" >
                <v-icon class="drawer-menu__branch-link-icon">mdi-rhombus-medium-outline</v-icon>
                <span @click="toggleHamburger">{{branch.title}} [{{branch.children_count}}] {{branch.is_unread}}</span>
              </div>
                </router-link>
            </div>
          </v-list-group>
        </v-list>
      </div>
    </div>
  </v-container>
  <!--
  <v-container class="pa-0" >
  <v-row
    no-gutters
    id="forum-drawer__main"
    align="stretch">
    <v-col
      cols="12"
      id="forum-drawer__header">
        <v-menu nudge-right="-12" v-if="allForums" offset-y>
        <template v-slot:activator="{ on }">
          <v-btn style="width: 100%" dark v-on="on">
            <span v-if="currentForum">{{currentForum.title}}</span>
          </v-btn>
        </template>
        <v-list >
          <v-list-item class="ma-0" v-for="forum in allForums" :key="forum.id" @click="setCurrentForum(forum)">
            <span >{{forum.title}}</span>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-col>
    <v-col
      cols="12"
      id="forum-drawer__body">
      <v-divider></v-divider>
         <ul v-if="currentForumBranches">
           <router-link v-for="branch in currentForumBranches"
            :to="{ name: 'Forum', params: { forumId: currentForum.id, branchId: branch.id }}"
            :key="branch.id"            >
            <li @click="setBranchInPrimary(true)"><span @click="toggleHamburger">{{branch.title}} [{{branch.children_count}}] {{branch.is_unread}}</span></li></router-link>
        </ul>
      </v-col>
    </v-row>
  </v-container>
  -->
</template>

<script>
export default {
  name: 'ForumDrawer',
  data () {
    return {
      navigationLinks: [
        { link: '/login/', title: 'Авторизация', icon: 'mdi-login' },
        { link: '/register/', title: 'Регистрация', icon: 'mdi-alpha-a' },
        { link: '/training/', title: 'Тренировка', icon: 'mdi-alpha-b' },
        { link: '/users/', title: 'Пользователи', icon: 'mdi-alpha-c' },
        { link: '/forum/', title: 'Форум', icon: 'mdi-alpha-d' },
        { link: '/forum/forum/add/', title: 'Новый форум', icon: 'mdi-alpha-e' },
        { link: '/forum/branch/add/', title: 'Новая ветка', icon: 'mdi-alpha-f' }
      ]
    }
  },
  computed: {
    allForums () {
      return this.$store.getters.getAllForumsList
    },
    currentForumBranches () {
      return this.$store.getters.getCurrentForumChildren
    },
    currentForum () {
      return this.$store.getters.getCurrentForum
    },
    currentBranch () {
      return this.$store.getters.getCurrentBranch
    },
    currentThread () {
      return this.$store.getters.getCurrentThread
    }
  },
  methods: {
    setBranchInPrimary (status) {
      this.$store.dispatch('setBranchInPrimary', status)
    },
    toggleHamburger () {
      if (document.documentElement.clientWidth < 595) {
        document.getElementById('hamburger').classList.toggle('is-active')
      }
    },
    async setCurrentForum (forum) {
      await this.$store.dispatch('setCurrentForum', forum)
      this.$store.dispatch('getForumValues', { currentForumId: forum.id })
    }
  }
}
</script>

<style scoped lang="scss">
  @import '../../styles/variables';

.forum-drawer__main {
  overflow: hidden;
  height: calc(100vh - #{$navigation-app-bar-height});
}
.forum-drawer__main *{
  color: #000000  !important;
}
.forum-drawer__main i{
  color: #F98500 !important;
}
.forum-drawer__header {
  background-color: $drawer__header__background-color;
  height: $view__header__height;
  color: $drawer__header__font-color;
}
.forum-drawer__body {
  height: calc(100vh - #{$navigation-app-bar-height} - #{$view__header__height});
  overflow-y: scroll;
}
.drawer-menu {
}
.drawer-menu a {
  display: flex;
  flex-direction: column;
  text-decoration: none;
  height: 100%;
  justify-content: center;
}
.drawer-menu__item {
}
.drawer-menu__group {
  background-color: white;
}
.drawer-menu__branch-link {
  width: 100%;
  display: inline-block;
  height: 30px;
}
.drawer-menu__branch-link:hover {
  background-color: $third-party;
  transition: 0.8s;
}
.drawer-menu__branch-link__active {
  background-color: $third-party;
  width: 100%;
  padding: 0;
}
.drawer-menu__branch-link-icon {
  margin-left: 20px;
  margin-right: 5px;
}

</style>
<style>
.v-application .primary--text {
caret-color:purple !important;
color: black !important;
}
</style>

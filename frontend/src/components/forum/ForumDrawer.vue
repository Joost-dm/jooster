<template>
  <v-container class="pa-0" >
  <v-row
    no-gutters
    id="forum-drawer__main"
    align="stretch">
    <v-col
      cols="12"
      id="forum-drawer__header">
        <v-menu v-if="allForums" offset-y>
        <template v-slot:activator="{ on }">
          <v-btn
            dark
            v-on="on"
          >
            <span v-if="currentForum">{{currentForum.title}}</span>
          </v-btn>
        </template>
        <v-list>
          <v-list-item v-for="forum in allForums" :key="forum.id" @click="setCurrentForum(forum)">
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
</template>

<script>
export default {
  name: 'ForumDrawer',
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
#forum-drawer__main {
  overflow: hidden;
}
#forum-drawer__header {
  background-color: $drawer__header__background-color;
  min-height: $view__header__height;
  color: $drawer__header__font-color;
}
#forum-drawer__body {
  height: calc(100vh - #{$navigation-app-bar-height} - #{$view__header__height});
  overflow-y: scroll;
  background-color: $color3;
}
</style>

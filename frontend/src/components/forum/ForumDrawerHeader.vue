<template>
  <div class="forum-drawer-header">
    <v-row class="forum-drawer-header__top">
      <v-menu
        class="forum-drawer-header__switch"
        v-if="currentForum && allForums"
        v-model="value"
        close-on-click
        close-on-content-click
        offset-y
      >
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            class="forum-drawer-header__switch-button"
            color="primary"
            v-bind="attrs"
            v-on="on"
          >
            <v-icon class="forum-drawer-header__lock-icon"
                    v-if="user
                    && currentForum
                    && currentForum.is_private
                    && (currentForum.members.indexOf(user.id) !== -1
                    || user.is_staff)">
              mdi-lock-open-variant
            </v-icon>
            <v-icon class="forum-drawer-header__lock-icon"
                    v-else-if="currentForum && currentForum.is_private">mdi-lock</v-icon>
            {{ currentForum.title }}
          </v-btn>
        </template>
        <v-list>
          <v-list-item
            v-for="forum in allForums"
            :key="forum.id"
            @click="setCurrentForum(forum)"
          >
            <v-icon class="forum-drawer-header__lock-icon"
                    v-if="user
                    && forum
                    && forum.is_private
                    && (forum.members.indexOf(user.id) !== -1
                    || user.is_staff)">
              mdi-lock-open-variant
            </v-icon>
            <v-icon class="forum-drawer-header__lock-icon" v-else-if="user && forum && forum.is_private">mdi-lock</v-icon>
            <v-list-item-title class="forum-drawer-header__switch-item">{{ forum.title }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
      <div class="forum-drawer-header__create-forum">
        <div class="forum-drawer-header__create-forum-button" @click="toggleForumCreateForm">
          <v-icon class="create-forum-button__icon">mdi-plus</v-icon>
        </div>
        <div class="forum-drawer-header__create-forum-form" ref="createForum">
          <forum-create></forum-create>
        </div>
      </div>
   </v-row>
  </div>
</template>

<script>
import ForumCreate from './ForumCreate'
export default {
  name: 'ForumDrawerHeader',
  components: {
    'forum-create': ForumCreate
  },
  data () {
    return {
      value: false
    }
  },
  computed: {
    user () {
      return this.$store.getters.getCurrentUser
    },
    allForums () {
      return this.$store.getters.getAllForumsList
    },
    currentForum () {
      return this.$store.getters.getCurrentForum
    }
  },
  methods: {
    toggleForumCreateForm () {
      this.$store.dispatch('toggleCreateForum')
    },
    async setCurrentForum (forum) {
      if (!forum.is_private ||
          forum.members.indexOf(this.user.id) !== -1 ||
          this.user.is_staff ||
          this.user.id === forum.author.id) {
        await this.$store.dispatch('setCurrentForum', forum)
        await this.$store.dispatch('getForumValues', { currentForumId: forum.id })
      }
    }
  },
  mounted () {
    this.$store.dispatch('setCreateForum', this.$refs.createForum)
  }
}
</script>

<style scoped lang="scss">
  @import '../../styles/variables';
  .forum-drawer-header {
    width: 100%;
    background-color: $drawer__header__background-color;
    height: $view__header__height;
    color: $drawer__header__font-color;
  }
  .forum-drawer-header__top {
    padding: 0 1rem 0 1rem;
    margin: 0;
    display: flex;
    flex-direction: row;
    width: 100%;
    justify-content: space-between;
    align-items: center;
    align-content: center;
    height: 100%;
  }
  .forum-drawer-header__switch {
  }
  .forum-drawer-header__title {
    color: $drawer__header__font-color;
  }
  .forum-drawer-header__switch-button {
    overflow: hidden;
    width: calc(100% - 3rem);
    font-size: 11px !important;
  }
  .forum-drawer-header__switch-button:hover {
    background-color: $hover;
  }
  .forum-drawer-header__switch-item {
    font-size: 14px;
  }
  .forum-drawer-header__create-forum {
    position: relative;
  }
  .forum-drawer-header__create-forum-button {
    display: flex;
    justify-content: center;
    align-content: center;
    height: 1.3em;
    width: 1.3em;
    background-color: $extra;
    border-radius: 50%;
    cursor: pointer;
    transition: 0.2s;
  }
  .forum-drawer-header__create-forum-button:hover {
    transform: scale(1.1);
  }
  .create-forum-button__icon {
    font-size: 20px !important;
  }
  .forum-drawer-header__create-forum-form {
    display: none;
    position: absolute;
    right: 0;
    top: 2em;
    min-width: 230px;
    background-color: $secondary;
    border: solid $third-party 1px;
    border-radius: 5px;
    z-index: 6;
  }
  .forum-drawer-header__forums-list {
    top: 1.5em;
    left: 0;
    z-index: 5;
    position: absolute;
    background-color: $secondary;
    width: 100%;
    overflow: hidden;
    height: 0;
    transition: 0.3s;
  }
  .forum-drawer-header__lock-icon {
    font-size: 1rem;
    margin-right: 0.3rem;
  }
  .forum-drawer-header__forums-list-item {
    padding-left: 1em;
    width: 100%;
    border: solid 1px $third-party;
    border-bottom: none;
    cursor: pointer;
  }
  .forum-drawer-header__forums-list:last-child {
    border-bottom: solid 1px $third-party;
  }
  .forum-drawer-header__forums-list-item:hover {
    background-color: $hover;
  }
</style>

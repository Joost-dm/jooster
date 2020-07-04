<template>
  <div class="forum-drawer-header">
    <v-row class="forum-drawer-header__top">
      <div class="forum-drawer-header__switch">
        <span class="forum-drawer-header__forum-title">{{currentForum.title}}</span>
        <div  class="forum-drawer-header__switch-button" @click="toggleForumsList">
          <v-icon v-if="!showForumsChoice" class="forum-drawer-header__button-icon">mdi-chevron-down</v-icon>
          <v-icon v-else class="forum-drawer-header__button-icon">mdi-chevron-up</v-icon>
        </div>
        <div class="forum-drawer-header__forums-list">
          <div v-for="forum in allForums" :key="forum.id" @click="setCurrentForum(forum)">
            <div v-if="forum !== currentForum" class="forum-drawer-header__forums-list-item">
              <span>{{forum.title}}</span>
            </div>
          </div>
        </div>
      </div>
      <div class="forum-drawer-header__create-forum-button">
        <v-icon class="create-forum-button__icon">mdi-plus</v-icon>
      </div>
   </v-row>
  </div>
</template>

<script>
export default {
  name: 'ForumDrawerHeader',
  data () {
    return {
      showForumsChoice: false
    }
  },
  computed: {
    allForums () {
      return this.$store.getters.getAllForumsList
    },
    currentForum () {
      return this.$store.getters.getCurrentForum
    }
  },
  methods: {
    toggleForumsList () {
      const forumsList = document.getElementsByClassName('forum-drawer-header__forums-list')[0]
      const forumsListElementHeight =
        document.getElementsByClassName('forum-drawer-header__switch')[0].offsetHeight + 1
      if (forumsList.style.height === '0px' || !forumsList.style.height) {
        forumsList.style.height = (forumsListElementHeight * (this.allForums.length - 1)) + 1 + 'px'
        this.showForumsChoice = true
      } else {
        forumsList.style.height = 0
        this.showForumsChoice = false
      }
    },
    async setCurrentForum (forum) {
      this.toggleForumsList()
      await this.$store.dispatch('setCurrentForum', forum)
      this.$store.dispatch('getForumValues', { currentForumId: forum.id })
    }
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
    margin: 0;
    display: flex;
    flex-direction: row;
    width: 100%;
    justify-content: space-between;
    padding: 0 1em 0 1em ;
    align-content: center;
    height: 100%;
  }
  .forum-drawer-header__switch {
    position: relative;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-content: center;
    padding-left: 1em;
    background-color: $secondary;
    width: 85%;
  }
  .forum-drawer-header__title {
    color: $drawer__header__font-color;
  }
  .forum-drawer-header__switch-button {
    display: flex;
    align-content: center;
    justify-content: center;
    transition: 0.1s;
    cursor: pointer;
  }
  .forum-drawer-header__switch-button:hover {
    background-color: $hover;
  }
  .forum-drawer-header__create-forum-button {
    margin-top: 3px;
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
  .forum-drawer-header__forums-list__displayed {
    height: auto;
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

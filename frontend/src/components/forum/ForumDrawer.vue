<template>
  <v-container fluid class="pa-0">
    <v-dialog class="v-dialog" v-model="usersList">
      <div class="dialog__content">
        <div class="dialog__header">
          <div class="dialog__title">
            <span>Участники форума</span>
          </div>
          <v-icon class="dialog__close_icon" @click="usersList=false">mdi-close</v-icon>
        </div>
        <div class="dialog__body">
          <users-list :type="'forum'" :action="'listUsers'"></users-list>
        </div>
      </div>
    </v-dialog>
    <v-dialog class="v-dialog" v-model="addUsersList">
      <div class="dialog__content">
        <div class="dialog__header">
          <div class="dialog__title">
            <span>Добавить участников</span>
          </div>
          <v-icon class="dialog__close_icon" @click="addUsersList=false">mdi-close</v-icon>
        </div>
        <div class="dialog__body">
          <users-list :type="'forum'" :action="'addUsers'"></users-list>
        </div>
      </div>
    </v-dialog>
    <v-dialog class="v-dialog"  v-model="branchCreation">
      <div class="dialog__content">
        <div class="dialog__header">
          <div class="dialog__title">
            <span>Новая ветка</span>
          </div>
          <v-icon class="dialog__close_icon" @click="branchCreation=false">mdi-close</v-icon>
        </div>
        <div class="dialog__body">
          <create-branch></create-branch>
        </div>
      </div>
    </v-dialog>
    <div class="forum-drawer__main">
      <drawer-header ></drawer-header>
      <div class="forum-drawer__body" >
        <v-list color="error" class="pa-0 drawer-menu">
          <v-list-group class="drawer-menu__group" >
            <template v-slot:activator>
              <v-list-item-icon>
                <v-icon>mdi-wrench-outline</v-icon>
              </v-list-item-icon>
              <v-list-item-title>Действия</v-list-item-title>
            </template>
            <div class="drawer-menu__item">
              <v-list-item @click="branchCreation=true">
                <v-list-item-icon>
                  <v-icon>mdi-plus</v-icon>
                </v-list-item-icon>
                <v-list-item-title>Создать ветку</v-list-item-title>
              </v-list-item>
            </div>
            <div class="drawer-menu__item">
              <v-list-item v-if="currentForum
                                && (currentForum.author.id === user.id
                                || user.is_staff)"
                           link
                           @click="addUsersList=true">
                <v-list-item-icon>
                  <v-icon>mdi-account-multiple-plus</v-icon>
                </v-list-item-icon>
                <v-list-item-title>Добавить участников</v-list-item-title>
              </v-list-item>
              <v-list-item v-else-if="currentForum && currentForum.is_private" link @click="usersList=true">
                <v-list-item-icon>
                  <v-icon>mdi-account-multiple</v-icon>
                </v-list-item-icon>
                <v-list-item-title>Участники</v-list-item-title>
              </v-list-item>
            </div>
            <div class="drawer-menu__item">
              <v-list-item v-if="currentForum
                                && (currentForum.author.id === user.id
                                || user.is_staff)"
                           link
                           @click="deleteCurrentForum">
                <v-list-item-icon>
                  <v-icon>mdi-delete</v-icon>
                </v-list-item-icon>
                <v-list-item-title>Удалить форум</v-list-item-title>
              </v-list-item>
            </div>
          </v-list-group>
          <v-list-group v-if="currentForum && currentForumBranches && currentForumBranches.length > 0"
                        value="true"
                        class="drawer-menu__group">
            <template v-slot:activator>
              <v-list-item-icon><v-icon>mdi-file-tree</v-icon></v-list-item-icon>
              <v-list-item-title>Ветки</v-list-item-title>
            </template>
            <div v-if="currentForumBranches">
              <div v-for="branch in currentForumBranches"
                   :key="branch.id"
                   class="drawer-menu__branch-link"
                   @click="clearUnread(branch)">
                <div class="drawer-menu__branch-link__disabled"
                     v-if="branch.is_private &&
                     branch.members.indexOf(user.id) === -1 &&
                     !user.is_staff">
                  <v-icon class="drawer-menu__branch-link-icon">mdi-lock</v-icon>
                  <span>{{branch.title}}</span>
                </div>
              <router-link v-else class="drawer-menu__branch-link__passive" active-class="drawer-menu__branch-link__active"
                :to="{ name: 'Forum', params: { forumId: currentForum.id, branchId: branch.id }}">
                <div @click="setBranchInPrimary(true)" >
                  <v-icon v-if="!branch.is_private" class="drawer-menu__branch-link-icon">mdi-text</v-icon>
                  <v-icon v-else-if="branch.members.indexOf(user.id) !== -1 || user.is_staff"
                          class="drawer-menu__branch-link-icon">mdi-lock-open-variant
                  </v-icon>
                  <span>{{branch.title}}</span>
                </div>
                <div v-if="branch.is_unread" class="branch-link-badge">
                  <span class="branch-link-badge__counter">{{branch.unread_count}}</span>
                </div>
              </router-link>
              </div>
            </div>
          </v-list-group>
          <div v-else class="drawer-menu__no-branches" >
            <span>Форум пуст</span>
          </div>
        </v-list>
      </div>
    </div>
  </v-container>
</template>

<script>
import ForumDrawerHeader from './ForumDrawerHeader'
import UsersList from '@/components/forum/UsersList'
import BranchCreate from '@/components/forum/BranchCreate'
export default {
  name: 'ForumDrawer',
  components: {
    'drawer-header': ForumDrawerHeader,
    'users-list': UsersList,
    'create-branch': BranchCreate
  },
  data () {
    return {
      addUsersList: false,
      usersList: false,
      branchCreation: false
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
    },
    user () {
      return this.$store.getters.getCurrentUser
    }
  },
  methods: {
    setBranchInPrimary (status) {
      this.$store.dispatch('setBranchInPrimary', status)
    },
    clearUnread (branch) {
      branch.is_unread = null
    },
    deleteCurrentForum () {
      this.$store.dispatch('deleteForum', this.currentForum)
    }
  }
}
</script>
<style lang="scss">
  @import '../../styles/variables';
.v-navigation-drawer--is-mobile {
  padding-top: 0 !important;
  top: $navigation-app-bar-height !important;
  height: calc(100vh - #{$navigation-app-bar-height}) !important;
}
.v-dialog {
  position: relative;
  max-width: 500px;
  max-height: 80%;
  background-color: $secondary;
  overflow: hidden;
}

.dialog__content {
  display: flex;
  flex-direction: column;
  align-items: center;
  overflow: hidden;
  height: 100%;
}

.dialog__header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  min-height: 45px;
  width: 100%;
  background-color: $primary;
}

.dialog__title {
  color: $secondary;
  font-size: 15px;
  margin-left: 0.7rem;
}
.dialog__close_icon {
  font-size: 20px !important;
  color: $extra !important;
  cursor: pointer;
  margin-right: 0.7rem;
}
.dialog__close_icon:hover {
  transition: 0.1s;
  transform: scale(1.3);
}
.dialog__body {
  display: flex;
  flex-direction: row;
  justify-content: center;
  width: 100%;
  height: calc(100% - 45px);
  overflow: hidden;

}

</style>
<style scoped lang="scss">
  @import '../../styles/variables';

.forum-drawer__main {
  overflow: hidden;
}
.forum-drawer__main *{
  color: #000000  !important;
}
.forum-drawer__main i{
  color: #F98500 !important;
}

.forum-drawer__body {
  overflow-y: auto;
  height: calc(100vh - #{$navigation-app-bar-height} - #{$view__header__height});
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
  display: flex;
  align-items: center;
  height: 35px;
  font-size: 13px;
  cursor: pointer;
}
.drawer-menu__branch-link:hover {
  background-color: $hover;
  transition: 0.2s;
}
.drawer-menu__branch-link__passive {
  width: 100%;
  padding-left: 1rem;
}
.drawer-menu__branch-link__active {
  background-color: $hover;
  width: 100%;
}
.drawer-menu__branch-link__disabled {
  padding-left: 1rem;
  cursor: pointer;
}
.drawer-menu__branch-link-icon {
  margin-left: 20px;
  margin-right: 5px;
  font-size: 18px !important;
}
.branch-link-badge {
  background-color: #F98500;
  border-radius: 50%;
  position: absolute;
  right: 20px;
  display: flex;
  min-width: 20px;
  height: 20px;
  justify-content: center;
  align-items: center;

}
.branch-link-badge__counter {
  color: #FFFFFF !important;
  font-size: 12px;
}
.drawer-menu__no-branches {
  background-color: $secondary;
  display: flex;
  width: 100%;
  align-items: center;
  justify-content: center;
}

</style>
<style>
.v-application .primary--text {
caret-color:purple !important;
color: black !important;
}
</style>

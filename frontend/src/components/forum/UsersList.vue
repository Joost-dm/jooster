<template>
  <div class="users_list">
    <div class="users_list__search">
      <div class="users_list__search_area">
        <input class="users_list__search_input" type="text" placeholder="Начните ввод имени">
        <div class="users_list__search_icon" @click="search">
          <v-icon>mdi-magnify</v-icon>
        </div>
      </div>
    </div>
    <div class="users_list__divider"></div>
    <div class="users_list__list">
      <div class="users_list__user_line" v-for="user in filteredList" :key="user.id">
        <div class="users_list__user_data">
          <img class="users_list__user_avatar" :src="user.avatar_url" alt="">
          <span class="users_list__user_name">{{user.displayed}}</span>
        </div>
        <div v-if="currentObject.members.indexOf(user.id) === -1
              && currentObject.is_private
              && user.id !== currentObject.author.id
              && (currentUser.id === currentObject.author.id
              || currentUser.is_staff)
              && action === 'addUsers'"
             @click="addMember(user)"
             class="users_list__add_button">
          <v-icon>mdi-plus</v-icon>
        </div>
        <div v-else-if="currentObject.is_private
              && user.id !== currentObject.author.id
              && (currentUser.id === currentObject.author.id
              || currentUser.is_staff)
              && action === 'addUsers'"
             @click="removeMember(user)"
             class="users_list__remove_button">
          <v-icon>mdi-close</v-icon>
        </div>
      </div>
      <div class="users_list__no_search_results" v-if="filteredList && !filteredList[0]">
        <span>Поиск не дал результатов.</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UsersList',
  props: ['type', 'action'],
  data () {
    return {
      filteredList: false
    }
  },
  computed: {
    currentUser () {
      return this.$store.getters.getCurrentUser
    },
    allUsersList () {
      return this.$store.getters.getUsersList
    },
    targetList () {
      if (this.action === 'addUsers' && this.allUsersList) {
        var targetList = []
        const otherUsers = []
        this.allUsersList.forEach(user => {
          if (this.currentObject.members.indexOf(user.id) !== -1) {
            targetList.push(user)
          } else {
            otherUsers.push(user)
          }
        })
        targetList = targetList.concat(otherUsers)
        return targetList
      } else if (this.action === 'listUsers' && this.allUsersList) {
        const targetList = []
        this.allUsersList.forEach(user => {
          if (this.currentObject.members.indexOf(user.id) !== -1) {
            targetList.push(user)
          }
        })
        return targetList
      } else {
        return []
      }
    },
    currentObject () {
      if (this.type === 'forum') {
        return this.$store.getters.getCurrentForum
      } else if (this.type === 'branch') {
        return this.$store.getters.getCurrentBranch
      } else {
        return {}
      }
    }
  },
  methods: {
    addMember (user) {
      if (this.type === 'forum') {
        this.$store.dispatch('addForumMember',
          { user: user, forum: this.$store.getters.getCurrentForum })
      } else if (this.type === 'branch') {
        this.$store.dispatch('addBranchMember',
          { user: user, branch: this.$store.getters.getCurrentBranch })
      }
    },
    removeMember (user) {
      if (this.type === 'forum') {
        this.$store.dispatch('removeForumMember',
          { user: user, forum: this.$store.getters.getCurrentForum })
      } else if (this.type === 'branch') {
        this.$store.dispatch('removeBranchMember',
          { user: user, branch: this.$store.getters.getCurrentBranch })
      }
    },
    search () {
      this.filteredList = this.targetList
      const searchValue = document.getElementsByClassName('users_list__search_input')[0].value.toUpperCase()
      this.filteredList = this.filteredList.filter(user => user.displayed.toUpperCase().startsWith(searchValue))
    }
  },
  async created () {
    await this.$store.dispatch('getUsersList')
    this.filteredList = this.targetList
  },
  mounted () {
    const searchInput = document.getElementsByClassName('users_list__search_input')[0]
    searchInput.addEventListener('keyup', this.search)
    this.filteredList = this.targetList
  }
}
</script>

<style scoped lang="scss">
@import "src/styles/variables";

.users_list {
  display: flex;
  flex-direction: column;
  justify-content: center;
  flex-wrap: nowrap;
  overflow: hidden;
  width: 100%;
  height: 100%;
}

.users_list__search {
  height: 50px;
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  padding: 5px 0 5px 0;
}
.users_list__search_area {
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 0 20px 0 20px;
  width: 90%;
  background-color: $hover;
  height: 90%;
  border-radius: 20px;
}
.users_list__search_input {
  width: 100%;
}
.users_list__search_input:active, :hover, :focus {
    outline: 0;
    outline-offset: 0;
}
.users_list__search_icon {
  transition: 0.2s;
  cursor: pointer;
}
.users_list__search_icon:hover {
  transition: 0.2s;
  transform: scale(1.2);
}
.users_list__no_search_results {
  display: flex;
  flex-direction: column;
  width: 100%;
  align-items: center;
  padding-top: 20px;
  color: $third-party;
}
.users_list__divider {
  height: 1px;
  width: 100%;
  background-color: $third-party;
}
.users_list__list {
  overflow-y: auto;
  overflow-x: hidden;
  height: calc(100% - 51px);
}
.users_list__user_line {
  padding: 0 3rem 0 1rem;
  align-items: center;
}
.users_list__user_line:hover {
  background-color: $hover;
}
.users_list__user_line {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  height: 50px;
  cursor: pointer;
}
.users_list__user_data {
  display: flex;
  flex-direction: row;
  align-items: center;
}
.users_list__user_name {
  font-size: 16px;
  padding-left: 0.5rem;
}
.users_list__user_avatar {
  height: 40px;
  border-radius: 5px;
  border: $third-party 1px solid;
}
.users_list__add_button {
    cursor: pointer;
}
.users_list__add_button i{
  color: $success;
}
.users_list__add_button i:hover {
  transform: scale(1.2);
}
.users_list__remove_button i {
  color: $error;
}
.users_list__remove_button i:hover {
  transform: scale(1.2);
}

</style>

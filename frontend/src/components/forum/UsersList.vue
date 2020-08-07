<template>
  <div class="users_list">
    <div class="users_list__search">
      <div class="users_list__search_area">
        <input class="users_list__search_input" type="text" placeholder="Начните ввод имени пользователя">
        <div class="users_list__search_icon">
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
        <div @click="addMemberToCurrentForum(user)" class="users_list__add_button">
          <v-icon>mdi-plus</v-icon>
        </div>
      </div>
      <div class="users_list__no_search_results" v-if="!filteredList[0]">
        <span>Поиск не дал результатов.</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UsersList',
  data () {
    return {
      filteredList: null
    }
  },
  computed: {
    usersList () {
      return this.$store.getters.getUsersList
    }
  },
  async created () {
    await this.$store.dispatch('getUsersList')
    this.filteredList = this.usersList
  },
  mounted () {
    const searchInput = document.getElementsByClassName('users_list__search_input')[0]
    searchInput.addEventListener('keyup', this.search)
  },
  methods: {
    addMemberToCurrentForum (user) {
      this.$store.dispatch('addForumMember', { user: user, forum: this.$store.getters.getCurrentForum })
    },
    search () {
      this.filteredList = this.usersList
      const searchValue = document.getElementsByClassName('users_list__search_input')[0].value.toUpperCase()
      this.filteredList = this.filteredList.filter(user => user.displayed.toUpperCase().startsWith(searchValue))
    }
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
.users_list__search_icon {
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
</style>

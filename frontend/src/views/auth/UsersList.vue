<template>
  <v-container fluid>
    <span v-for="user in usersList" :key="user.id">{{user.displayed}}<v-btn @click="addMemberToCurrentForum(user)">add</v-btn><br></span>
  </v-container>
</template>

<script>
export default {
  name: 'UsersList',
  computed: {
    usersList () {
      return this.$store.getters.getUsersList
    }
  },
  created () {
    this.$store.dispatch('getUsersList')
  },
  methods: {
    addMemberToCurrentForum (user) {
      this.$store.dispatch('addForumMember', { user: user, forum: this.$store.getters.getCurrentForum })
    }
  }
}
</script>

<style scoped>

</style>

<template>
  <v-container fluid class="pa-0">
    <v-text-field v-model="newBranch.title" label="title"></v-text-field>
    <v-checkbox v-model="newBranch.is_private" label="Приватный"></v-checkbox>
    <v-btn @click="createBranch">Создать</v-btn>
  </v-container>
</template>

<script>
export default {
  name: 'BranchCreate',
  data () {
    return {
      newBranch: {
        title: null,
        is_private: null,
        parent_forum: null
      }
    }
  },
  methods: {
    async createBranch () {
      this.newBranch.parent_forum = this.$store.getters.getCurrentForum.id
      await this.$store.dispatch('createBranch', this.newBranch)
      await this.$store.dispatch('getForumChildren', this.$store.getters.getCurrentForum)
    }
  }
}
</script>

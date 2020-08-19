<template>
  <v-container class="pa-0 branch-create">
    <div class="branch-create__form">
      <v-text-field class="branch-create__title-input" counter="20" v-model="newBranch.title" label="Название"></v-text-field>
      <v-checkbox class="branch-create__private-checkbox"  v-model="newBranch.is_private" label="Приватная ветка"></v-checkbox>
      <v-btn color="primary" @click="createBranch" class="branch-create__submit-button">Создать</v-btn>
    </div>

  </v-container>
</template>

<script>
export default {
  name: 'BranchCreate',
  data () {
    return {
      newBranch: {
        title: null,
        is_private: false,
        parent_forum: null
      }
    }
  },
  computed: {
    currentForum () {
      return this.$store.getters.getCurrentForum
    },
    currentBranch () {
      return this.$store.getters.getCurrentBranch
    }
  },
  methods: {
    async createBranch () {
      this.newBranch.parent_forum = this.$store.getters.getCurrentForum.id
      await this.$store.dispatch('createBranch', this.newBranch)
      await this.$store.dispatch('getForumChildren', this.$store.getters.getCurrentForum)
      await this.$router.push('/forum/' + this.currentForum.id + '/' + this.currentBranch.id + '/')
    }
  }
}
</script>
<style scoped lang="scss">
@import '../../styles/variables';
.branch-create {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  overflow: hidden;
}
.branch-create__form {
  display: flex;
  flex-direction: column;
  width: 100%;
  padding: 2rem 1rem 3rem 1rem;
}
.branch-create__title-input {
}
.branch-create__private-checkbox {
}
.branch-create__submit-button {
  width: 200px;
}
</style>

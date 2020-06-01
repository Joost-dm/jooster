<template>
<v-container class="pa-0" mb-5>
  <hr>
  <div style="height: 150px; background-color: gainsboro"><b>{{post.text}}</b></div>
  <hr>
  <span>likes: {{post.likes.length}}</span>
  <br>
  <v-btn @click="toggleLikePost(post)">like</v-btn>
  <v-btn v-if="user.id === post.author" @click="deletePost(post)">удалить</v-btn>
  <router-link
    v-if="type === 'thread'"
    :to="{
    name: 'Forum',
    params: {
      forumId: currentForum.id,
      branchId: currentBranch.id,
      threadId: post.id
    }}">
   <span @click="setBranchInPrimary(false)">Обсуждение [{{post.children_count}}] {{post.is_unread}}</span>
  </router-link>
</v-container>
</template>

<script>
export default {
  name: 'ForumPost',
  props: ['post', 'type'],
  computed: {
    user () {
      return this.$store.getters.getCurrentUser
    },
    currentBranch () {
      return this.$store.getters.getCurrentBranch
    },
    currentForum () {
      return this.$store.getters.getCurrentForum
    }
  },
  methods: {
    deletePost (post) {
      if (this.type === 'post') {
        this.$store.dispatch('deletePost', post)
      } else if (this.type === 'thread') {
        this.$store.dispatch('deleteThread', post)
      }
    },
    toggleLikePost (post) {
      if (post.likes.indexOf(this.$store.getters.getCurrentUser.id) === -1) {
        if (this.type === 'post') {
          this.$store.dispatch('likePost', post)
        } else if (this.type === 'thread') {
          this.$store.dispatch('likeThread', post)
        }
      } else {
        if (this.type === 'post') {
          this.$store.dispatch('dislikePost', post)
        } else if (this.type === 'thread') {
          this.$store.dispatch('dislikeThread', post)
        }
      }
    },
    setBranchInPrimary (status) {
      this.$store.dispatch('setBranchInPrimary', status)
    }
  }
}
</script>

<style scoped>

</style>

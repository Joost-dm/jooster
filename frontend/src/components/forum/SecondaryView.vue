<template>
  <v-container class="pa-0" >
  <v-row
    no-gutters
    id="thread__main"
    align="stretch">
    <v-col
      cols="12"
      id="secondary-view__header">
      <span v-if="currentThread">Тема: #{{currentThread.id}}</span>
      <v-spacer></v-spacer>
      <div @click="refreshThread" class="secondary-view__header-refresh-button">
        <v-icon>mdi-refresh</v-icon>
      </div>
    </v-col>
    <v-col
      cols="12"
      id="secondary-view__posts-body" @scroll="postsScrollHandler">
       <forum-post v-if="!threadNextPageUrl && currentThread"
                   :post="currentThread" threadStarter="true" :type="'thread'"></forum-post>
      <div id="secondary__posts">
        <local-loader v-if="secondaryLoading"></local-loader>
        <forum-post v-for="post in currentThreadPosts" :post="post" :key="post.id" :type="'post'" ></forum-post>
      </div>
      <v-col
      cols="12"
      id="secondary-view__bottom-form">
        <post-form :type="'post'"></post-form>
      </v-col>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import ForumPost from './Post'
import LocalLoader from '../loaders/LocalLoader'
import PostForm from './PostForm'

export default {
  name: 'SecondaryView',
  components: {
    'forum-post': ForumPost,
    'local-loader': LocalLoader,
    'post-form': PostForm
  },
  computed: {
    currentThread () {
      return this.$store.getters.getCurrentThread
    },
    currentThreadPosts () {
      return this.$store.getters.getCurrentThreadChildren
    },
    currentForum () {
      return this.$store.getters.getCurrentForum
    },
    currentBranch () {
      return this.$store.getters.getCurrentBranch
    },
    threadNextPageUrl () {
      return this.$store.getters.getThreadNextPageUrl
    },
    currentThreadScrollStart () {
      return this.$store.getters.getCurrentThreadScrollStart
    },
    secondaryLoading () {
      return this.$store.getters.secondaryLoading
    }
  },
  methods: {
    async threadNextPage () {
      if (this.threadNextPageUrl) {
        const currentThread = this.$store.getters.getCurrentThread
        await this.$store.dispatch('getThreadChildren', { thread: currentThread, url: this.threadNextPageUrl })
      }
    },
    async postsScrollHandler () {
      const postsBody = document.getElementById('secondary-view__posts-body')
      if (postsBody.scrollTop <= 20 && postsBody.scrollTop > 0 && !this.preventThreadScrollTrigger) {
        this.preventThreadScrollTrigger = true
        const postsBody = document.getElementById('secondary-view__posts-body')
        this.$store.dispatch('setCurrentThreadBottomScroll', postsBody.scrollHeight + 100)
        await this.threadNextPage()
        this.preventThreadScrollTrigger = false
      }
    },
    updateComponentScrollController () {
      const postsList = document.getElementById('secondary__posts')
      const postsBody = document.getElementById('secondary-view__posts-body')
      if (postsBody) {
        postsBody.scrollTop = postsBody.scrollHeight - this.$store.getters.getCurrentThreadBottomScroll
      }
      if (this.currentThreadScrollStart && postsList && !this.secondaryLoading) {
        postsList.scrollIntoView(false)
        this.$store.dispatch('setCurrentThreadBottomScroll', null)
        postsBody.scrollTop = postsBody.scrollHeight
        this.$store.dispatch('setCurrentThreadScrollStart', false)
      }
    },
    refreshThread () {
      this.$store.dispatch('clearThreadChildren')
      const currentThread = this.$store.getters.getCurrentThread
      if (currentThread) {
        this.$store.dispatch('getThreadChildren', { thread: currentThread })
      }
    }
  },
  updated () {
    this.updateComponentScrollController()
  }
}
</script>

<style scoped lang="scss">
  @import '../../styles/variables';
#secondary-view-main {
  overflow: hidden;
}
#secondary-view__header {
  z-index: 3;
  display: flex;
  justify-content: space-between;
  background-color: $view__header__background-color;
  min-height: $view__header__height;
  color: $view__header__font-color;
}
#secondary-view__posts-body {
  height: calc(100vh - #{$navigation-app-bar-height} - #{$view__header__height});
  overflow-y: scroll;
  background-color: $text-background;
}
#secondary-view__bottom-form {
  min-height: $topic-bottom-form-height;
}
.secondary-view__header-refresh-button {
  display: flex;
  align-content: center;
  justify-content: center;
  cursor: pointer;
  margin-right: 30px;
}
.secondary-view__header-refresh-button i {
    color: $third-party;
}
.secondary-view__header-refresh-button i:hover {
  color: $extra;
}
</style>

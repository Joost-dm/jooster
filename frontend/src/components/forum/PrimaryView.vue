<template>
  <v-container class="pa-0" >
  <!----------------------------------------------------------------->
    <v-row
    v-if="branchInPrimary"
    no-gutters
    class="primary-view__main"
    align="stretch">
    <v-col
      cols="12"
      class="primary-view__header">
      <span v-if="currentBranch" >{{currentBranch.title}}</span>
    </v-col>
    <v-col
      cols="12"
      class="primary-view__body" id="primary-view__threads-body" @scroll="threadsScrollHandler">
      <div id="primary__threads" v-if="currentBranchThreads">
        <local-loader v-if="primaryLoading"></local-loader>
        <forum-post v-for="thread in currentBranchThreads" :key="thread.id" :post="thread" :type="'thread'"></forum-post>
       </div>
      </v-col>
      <!-- ФОРМА -->
      <post-form :type="'thread'"></post-form>
    </v-row>
    <!----------------------------------------------------------------->
     <v-row
    v-else
    no-gutters
    class="primary-view__main"
    align="stretch">
    <v-col
      cols="12"
      class="primary-view__header">
      <span v-if="currentThread">{{currentThread.text}}</span><br>
      <v-btn @click="setBranchInPrimary(true)"><v-icon>mdi-arrow-left</v-icon></v-btn>
    </v-col>
    <v-col
      cols="12"
      class="primary-view__body" id="primary-view__posts-body" @scroll="postsScrollHandler">
       <hr>
        <b v-if="!threadNextPageUrl && currentThread">{{currentThread.text}}</b>
        <hr>
       <div id="primary__posts" v-if="currentThreadPosts">
         <local-loader v-if="primaryLoading"></local-loader>
         <forum-post v-for="post in currentThreadPosts" :post="post" :key="post.id" :type="'post'"></forum-post>
       </div>
      </v-col>
       <!-- ФОРМА -->
      <v-col
      cols="12"
      class="primary-view__bottom-form">
      <post-form :type="'post'"></post-form>
      </v-col>
    </v-row>
    <!----------------------------------------------------------------->
  </v-container>
</template>
<script>
import ForumPost from './Post'
import LocalLoader from '../loaders/LocalLoader'
import PostForm from './PostForm'

export default {
  name: 'PrimaryView',
  components: {
    'forum-post': ForumPost,
    'local-loader': LocalLoader,
    'post-form': PostForm
  },
  data () {
    return {
      preventBranchScrollTrigger: false,
      preventThreadScrollTrigger: false
    }
  },
  computed: {
    branchInPrimary () {
      return this.$store.getters.getBranchInPrimary
    },
    currentBranchThreads () {
      return this.$store.getters.getCurrentBranchChildren
    },
    currentThreadPosts () {
      return this.$store.getters.getCurrentThreadChildren
    },
    currentThread () {
      return this.$store.getters.getCurrentThread
    },
    currentBranch () {
      return this.$store.getters.getCurrentBranch
    },
    currentForum () {
      return this.$store.getters.getCurrentForum
    },
    threadNextPageUrl () {
      return this.$store.getters.getThreadNextPageUrl
    },
    branchNextPageUrl () {
      return this.$store.getters.getBranchNextPageUrl
    },
    currentBranchScrollStart () {
      return this.$store.getters.getCurrentBranchScrollStart
    },
    currentThreadScrollStart () {
      return this.$store.getters.getCurrentThreadScrollStart
    },
    primaryLoading () {
      return this.$store.getters.primaryLoading
    }
  },
  methods: {
    setBranchInPrimary (status) {
      this.$store.dispatch('setBranchInPrimary', status)
    },
    async threadNextPage () {
      if (this.threadNextPageUrl) {
        const currentThread = this.$store.getters.getCurrentThread
        await this.$store.dispatch(
          'getThreadChildren',
          { thread: currentThread, url: this.threadNextPageUrl }
        )
      }
    },
    async branchNextPage () {
      if (this.branchNextPageUrl) {
        const currentBranch = this.$store.getters.getCurrentBranch
        await this.$store.dispatch(
          'getBranchChildren',
          { branch: currentBranch, url: this.branchNextPageUrl }
        )
      }
    },
    async threadsScrollHandler () {
      const threadsBody = document.getElementById('primary-view__threads-body')
      if (threadsBody.scrollTop <= 10 && threadsBody.scrollTop > 0 && !this.preventBranchScrollTrigger) {
        this.preventBranchScrollTrigger = true
        const threadsBody = document.getElementById('primary-view__threads-body')
        this.$store.dispatch('setCurrentBranchBottomScroll', threadsBody.scrollHeight + 100)
        await this.branchNextPage()
        this.preventBranchScrollTrigger = false
      }
    },
    async postsScrollHandler () {
      const postsBody = document.getElementById('primary-view__posts-body')
      if (postsBody.scrollTop <= 10 && postsBody.scrollTop > 0 && !this.preventThreadScrollTrigger) {
        this.preventThreadScrollTrigger = true
        const postsBody = document.getElementById('primary-view__posts-body')
        this.$store.dispatch('setCurrentThreadBottomScroll', postsBody.scrollHeight + 100)
        await this.threadNextPage()
        this.preventThreadScrollTrigger = false
      }
    },
    updateComponentScrollController () {
      const threadsList = document.getElementById('primary__threads')
      const postsList = document.getElementById('primary__posts')
      const threadsBody = document.getElementById('primary-view__threads-body')
      const postsBody = document.getElementById('primary-view__posts-body')
      if (threadsBody) {
        threadsBody.scrollTop = threadsBody.scrollHeight - this.$store.getters.getCurrentBranchBottomScroll
      } else if (postsBody) {
        postsBody.scrollTop = postsBody.scrollHeight - this.$store.getters.getCurrentThreadBottomScroll
      }
      if (this.currentBranchScrollStart && threadsList && !this.primaryLoading) {
        threadsList.scrollIntoView(false)
        this.$store.dispatch('setCurrentBranchBottomScroll', null)
        threadsBody.scrollTop = threadsBody.scrollHeight
        this.$store.dispatch('setCurrentBranchScrollStart', false)
      } else if (this.currentThreadScrollStart && postsList && !this.primaryLoading) {
        postsList.scrollIntoView(false)
        this.$store.dispatch('setCurrentThreadBottomScroll', null)
        postsBody.scrollTop = postsBody.scrollHeight
        this.$store.dispatch('setCurrentThreadScrollStart', false)
      }
    },
    formResizeHandler () {
      const appBarHeight = document.getElementById('v-app-bar').clientHeight
      const main = document.getElementsByClassName('primary-view__main')[0]
      main.style.height = 'calc(100vh - ' + appBarHeight + 'px;)'
      const mainHeight = document.getElementsByClassName('primary-view__main')[0].clientHeight
      const headerHeight = document.getElementsByClassName('primary-view__header')[0].clientHeight
      const formHeight = document.getElementsByClassName('primary-view__bottom-form')[0].clientHeight
      const body = document.getElementsByClassName('primary-view__body')[0]
      body.style.height = (mainHeight - headerHeight - formHeight) + 'px'
    }
  },
  mounted () {
    document.getElementsByClassName('primary-view__bottom-form')[0].addEventListener('keyup', this.formResizeHandler)
  },
  updated () {
    this.updateComponentScrollController()
  }
}
</script>
<style scoped lang="scss">
  @import '../../styles/variables';
.primary-view__main {
  overflow: hidden;
  height: calc(100vh - #{$navigation-app-bar-height});
}
.primary-view__header {
  background-color: $view__header__background-color;
  height: $view__header__height;
  color: $view__header__font-color;
}
.primary-view__body {
  height: calc(100vh - #{$navigation-app-bar-height} - #{$view__header__height} - #{$topic-bottom-form-height});
  overflow-y: scroll;
  overflow-x: hidden;
  background-color: $text-background;
}

</style>

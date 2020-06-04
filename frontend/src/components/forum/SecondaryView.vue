<template>
  <v-container class="pa-0" >
  <v-row
    no-gutters
    id="thread__main"
    align="stretch">
    <v-col
      cols="12"
      id="secondary-view__header">
      <span v-if="currentThread">{{currentThread.text}}</span>
    </v-col>
    <v-col
      cols="12"
      id="secondary-view__posts-body" @scroll="postsScrollHandler">
      <hr>
      <b v-if="!threadNextPageUrl && currentThread">{{currentThread.text}}</b>
      <hr>
      <div id="secondary__posts">
        <forum-post v-for="post in currentThreadPosts" :post="post" :key="post.id" :type="'post'"></forum-post>
      </div>
      <v-col
      cols="12"
      id="secondary-view__bottom-form">
        <v-container fluid class="pa-0">
          <v-text-field
          v-model="newPost.text" label="Сообщение"></v-text-field>
          <v-btn @click="createPost">Создать</v-btn>
        </v-container>
      </v-col>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import ForumPost from './ForumPost'

export default {
  name: 'SecondaryView',
  data () {
    return {
      newPost: {
        text: null,
        parent: null
      },
      preventThreadScrollTrigger: false
    }
  },
  components: {
    'forum-post': ForumPost
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
    }
  },
  methods: {
    createPost () {
      this.newPost.parent_thread = this.currentThread.id
      this.$store.dispatch('createPost', this.newPost)
    },
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
        this.$store.dispatch('setCurrentThreadBottomScroll', postsBody.scrollHeight)
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
      if (this.currentThreadScrollStart && postsList) {
        postsList.scrollIntoView(false)
        this.$store.dispatch('setCurrentThreadBottomScroll', null)
        postsBody.scrollTop = postsBody.scrollHeight
        this.$store.dispatch('setCurrentThreadScrollStart', false)
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
</style>

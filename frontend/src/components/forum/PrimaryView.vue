<template>
  <v-container class="pa-0" >
    <v-dialog class="v-dialog" v-model="usersList">
      <div class="dialog__content">
        <div class="dialog__header">
          <div class="dialog__title">
            <span>Участники ветки</span>
          </div>
          <v-icon class="dialog__close_icon" @click="usersList=false">mdi-close</v-icon>
        </div>
        <div class="dialog__body">
          <users-list :type="'branch'" :action="'listUsers'"></users-list>
        </div>
      </div>
    </v-dialog>
    <v-dialog class="v-dialog" v-model="addUsersList">
      <div class="dialog__content">
        <div class="dialog__header">
          <div class="dialog__title">
            <span>Добавить участника</span>
          </div>
          <v-icon class="dialog__close_icon" @click="addUsersList=false">mdi-close</v-icon>
        </div>
        <div class="dialog__body">
          <users-list :type="'branch'" :action="'addUsers'"></users-list>
        </div>
      </div>
    </v-dialog>
    <v-row
    v-if="branchInPrimary"
    no-gutters
    class="primary-view__main"
    align="stretch">
    <v-col
      cols="12"
      class="primary-view__header">
      <div class="header__info">
        <div class="header__title">
          <span v-if="currentBranch" >#{{currentBranch.title.toLowerCase()}}</span>
        </div>
        <div v-if="currentBranch" class="header__subtitle">
          <div v-if="currentBranch.is_private" class="header__subtitle-content">
             <span>закрытая ветка</span>
            <div v-if="user && currentBranch && (user.id === currentBranch.author.id || user.is_staff)"
                 class="subtitle-members-counter"
                 @click="addUsersList=true">
              <v-icon class="subtitle-members-counter__icon">mdi-account-multiple</v-icon>
              <span class="subtitle-members-counter__count">{{currentBranch.members.length}}</span>
              <v-icon class="subtitle-members-counter__icon subtitle-members-counter__add-member-button">mdi-plus
              </v-icon>
            </div>
            <div v-else class="subtitle-members-counter" @click="usersList=true">
              <v-icon class="subtitle-members-counter__icon">mdi-account-multiple</v-icon>
              <span class="subtitle-members-counter__count">{{currentBranch.members.length}}</span>
            </div>
          </div>
          <div v-else class="header__subtitle-content">открытая ветка</div>
          <div v-if="user.id === currentBranch.author.id || user.is_staff" @click="deleteBranch" class="primary-view__header-delete-button">
            <v-icon>mdi-delete</v-icon>
          </div>
        </div>
      </div>
      <div @click="refreshBranch" class="primary-view__header-button">
        <v-icon>mdi-refresh</v-icon>
      </div>
    </v-col>
    <v-col
      cols="12"
      class="primary-view__body" id="primary-view__threads-body" ref="threadsBody" @scroll="threadsScrollHandler">
      <div id="primary__threads" ref="threads" v-if="currentBranchThreads">
        <local-loader v-if="primaryLoading"></local-loader>
        <forum-post v-for="thread in currentBranchThreads" :key="thread.id" :post="thread" :type="'thread'"></forum-post>
       </div>
      </v-col>
      <post-form class="primary-view__bottom-form" v-if="branchInPrimary" :type="'thread'"></post-form>
    </v-row>
     <v-row
    v-else
    no-gutters
    class="primary-view__main"
    align="stretch">
    <v-col
      cols="12"
      class="primary-view__header">
      <div class="header__info">
        <div class="header__title">
          <span v-if="currentThread">обсуждение #{{currentThread.id}}</span>
        </div>
        <div class="header__subtitle header__subtitle__link">
          <span v-if="currentThread"
                @click="setParrentBranchInPrimary">
            #{{currentThread.parent_branch_title.toLowerCase()}}
          </span>
        </div>
      </div>
      <div @click="setBranchInPrimary(true)" class="header__back-button">
        <v-icon >mdi-arrow-left</v-icon>
      </div>
      <div @click="refreshThread" class="primary-view__header-button">
        <v-icon>mdi-refresh</v-icon>
      </div>
    </v-col>
    <v-col
      cols="12"
      class="primary-view__body" id="primary-view__posts-body" ref="postsBody" @scroll="postsScrollHandler">
        <forum-post v-if="!threadNextPageUrl && currentThread" :post="currentThread" threadStarter="true" :type="'post'"></forum-post>
       <div id="primary__posts" ref="posts" v-if="currentThreadPosts">
         <local-loader v-if="primaryLoading"></local-loader>
         <forum-post v-for="post in currentThreadPosts" :post="post" :key="post.id" :type="'post'"></forum-post>
       </div>
      </v-col>
      <post-form class="primary-view__bottom-form" v-if="!branchInPrimary" :type="'post'"></post-form>
    </v-row>
  </v-container>
</template>
<script>
import ForumPost from './Post'
import LocalLoader from '../loaders/LocalLoader'
import PostForm from './PostForm'
import UsersList from '@/components/forum/UsersList'

export default {
  name: 'PrimaryView',
  components: {
    'forum-post': ForumPost,
    'local-loader': LocalLoader,
    'post-form': PostForm,
    'users-list': UsersList
  },
  data () {
    return {
      preventBranchScrollTrigger: false,
      preventThreadScrollTrigger: false,
      usersList: false,
      addUsersList: false
    }
  },
  computed: {
    user () {
      return this.$store.getters.getCurrentUser
    },
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
      const threadsBody = this.$refs.threadsBody
      if (threadsBody.scrollTop <= 10 && threadsBody.scrollTop > 0 && !this.preventBranchScrollTrigger) {
        this.preventBranchScrollTrigger = true
        this.$store.dispatch('setCurrentBranchBottomScroll', threadsBody.scrollHeight + 100)
        await this.branchNextPage()
        this.preventBranchScrollTrigger = false
      }
    },
    async postsScrollHandler () {
      const postsBody = this.$refs.postsBody
      if (postsBody.scrollTop <= 10 && postsBody.scrollTop > 0 && !this.preventThreadScrollTrigger) {
        this.preventThreadScrollTrigger = true
        this.$store.dispatch('setCurrentThreadBottomScroll', postsBody.scrollHeight + 100)
        await this.threadNextPage()
        this.preventThreadScrollTrigger = false
      }
    },
    updateComponentScrollController () {
      const threadsList = this.$refs.threads
      const postsList = this.$refs.posts
      const threadsBody = this.$refs.threadsBody
      const postsBody = this.$refs.postsBody
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
    refreshBranch () {
      this.$store.dispatch('clearBranchChildren')
      const currentBranch = this.$store.getters.getCurrentBranch
      if (currentBranch) {
        this.$store.dispatch('getBranchChildren', { branch: currentBranch })
      }
    },
    refreshThread () {
      this.$store.dispatch('clearThreadChildren')
      const currentThread = this.$store.getters.getCurrentThread
      if (currentThread) {
        this.$store.dispatch('getThreadChildren', { thread: currentThread })
      }
    },
    async setParrentBranchInPrimary () {
      this.$store.dispatch('setBranchInPrimary', true)
      this.$store.dispatch('getCurrentBranchById', this.currentThread.parent_branch)
    },
    mobileScreenHeightController () {
      try {
        const viewportHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0)
        const appBarHeight = document.getElementById('v-app-bar').offsetHeight
        const headerHeight = document.getElementsByClassName('primary-view__header')[0].offsetHeight
        const bottomFormHeight = document.getElementsByClassName('primary-view__bottom-form')[0].offsetHeight
        const primaryBody = document.getElementsByClassName('primary-view__body')[0]
        const mobileForumDrawer = document.getElementsByClassName('v-navigation-drawer--is-mobile')[0]
        const apiInfo = document.getElementsByClassName('api-info')[0]
        const apiInfoUpButton = document.getElementsByClassName('api-info__up-button')[0]
        primaryBody.style.height = (viewportHeight - appBarHeight - headerHeight - bottomFormHeight) + 'px'
        const screenWithoutAppBarHeight = (viewportHeight - appBarHeight)
        mobileForumDrawer.style.height = screenWithoutAppBarHeight + 'px'
        apiInfo.style.height = screenWithoutAppBarHeight + 'px'
        apiInfoUpButton.style.top = screenWithoutAppBarHeight - 40 + 'px'
      } catch (error) {
        error.message = null
      }
    },
    async deleteBranch () {
      await this.$store.dispatch('deleteBranch', this.currentBranch)
    }
  },
  updated () {
    this.updateComponentScrollController()
  },
  mounted () {
    this.mobileScreenHeightController()
    window.addEventListener('resize', this.mobileScreenHeightController)
  }
}
</script>
<style scoped lang="scss">
  @import '../../styles/variables';
.primary-view__main {
  position: relative;
  overflow: hidden;
  width: 100%;
}
.primary-view__header {
  z-index: 3;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  background-color: $view__header__background-color;
  height: $view__header__height;
  color: $view__header__font-color;
}

.header__info {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-content: center;
  width: 100%;
  height: 100%;
}

.header__title {
  display: flex;
  justify-content: flex-start;
  padding-left: 2rem;
  font-size: 14px;
  color: $secondary;
}
.header__subtitle {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  padding-left: 2rem;
  font-size: 14px;
  color: $third-party;
}

.header__subtitle-content {
  display: flex;
  flex-direction: row;
}
.header__subtitle__link span:hover {
  transition: 0.3s;
  cursor: pointer;
  color: $extra;
}
.subtitle-members-counter {
  color: $third-party;
  cursor: pointer;
  margin-left: 0.5rem;
}
.subtitle-members-counter:hover {
  color: $extra;
}
.subtitle-members-counter__icon {
  color: inherit;
  font-size: 18px;
}
.subtitle-members-counter__count {
  font-size: 12px;
}
.subtitle-members-counter__add-member-button {
  cursor: pointer;
}
.subtitle-members-counter__add-member-button:hover {
  color: $extra;
}
.header__back-button {
  display: flex;
  align-content: center;
  justify-content: center;
  cursor: pointer;
  margin-right: 2rem;
}
.header__back-button i {
    color: $third-party ;
}
.header__back-button i:hover {
    color: $extra;
}
.primary-view__header-button {
  display: flex;
  align-content: center;
  justify-content: center;
  cursor: pointer;
  margin-right: 30px;
}

.primary-view__header-button i {
    color: $third-party;
}
.primary-view__header-button i:hover {
    color: $extra;
}

.primary-view__header-delete-button i {
  color: $third-party;
  cursor: pointer;
  font-size: 1rem;
  margin-left: 0.7rem;
  transition: 0.2s;
}
.primary-view__header-delete-button  i:hover {
  color: $error;
  transform: scale(1.2);
}
.primary-view__body {
  height: calc(100vh - #{$navigation-app-bar-height} - #{$view__header__height} - #{$topic-bottom-form-height});
  overflow-y: scroll;
  overflow-x: hidden;
  background-color: $text-background;
  margin-bottom: $topic-bottom-form-height;
}
.primary-view__bottom-form {
  position: absolute;
  width: 98%;
  margin: 0 1% 0 1%;
  bottom: 0;
}

</style>

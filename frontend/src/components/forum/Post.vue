<template>
  <v-container fluid class="post" :class="postClass">
    <div class="post__left-side">
      <v-avatar class="post__avatar">
        <v-img :src=post.author.avatar_url></v-img>
      </v-avatar>
      <span class="post__user_rating">{{post.author.carma}}</span>
      <div  class="post__rating_options">
        <div v-if="user.id === post.author.id"
             class="post__rating_icon disabled_icon">
          <v-icon>mdi-minus</v-icon>
        </div>
        <div v-else-if="post.users_disliked_list.indexOf(user.id) !== -1"
             class="post__rating_icon rating_minus rating_disliked">
          <v-icon>mdi-minus</v-icon>
        </div>
        <div v-else class="post__rating_icon rating_minus" @click="dislikePost(post)">
          <v-icon>mdi-minus</v-icon>
        </div>
        <span class="post__post_rating">{{post.carma}}</span>
        <div v-if="user.id === post.author.id"
             class="post__rating_icon disabled_icon">
          <v-icon>mdi-plus</v-icon>
        </div>
        <div v-else-if="post.users_liked_list.indexOf(user.id) !== -1"
             class="post__rating_icon rating_plus rating_liked">
          <v-icon>mdi-plus</v-icon>
        </div>
        <div v-else class="post__rating_icon rating_plus" @click="likePost(post)">
          <v-icon>mdi-plus</v-icon>
        </div>
      </div>
    </div>
    <div class="post__right-side">
      <div class="post__header">
        <div class="post__author">
          <span>{{post.author.displayed}}</span>
        </div>
        <div class="post__pub-date">
          <span>{{dateRefactor(post.pub_date)}}</span>
        </div>
      </div>
      <div class="post__divider">
        <div class="post__divider-part1"></div>
        <div class="post__divider-part2"></div>
      </div>
      <div class="post__body">
        <p class="post__text" :class="postTextClass">{{post.text}}</p>
      </div>
      <div class="post__footer">
        <div class="post__discussion" @click="clearUnread(post)">
          <router-link
            v-if="type === 'thread' && !threadStarter"
            :to="{
            name: 'Forum',
            params: {
              forumId: currentForum.id,
              branchId: currentBranch.id,
              threadId: post.id
            }}">
             <div @click="setBranchInPrimary(false)">
               <span class="post__discussion-link">обсуждение: {{post.children_count}}</span>
               <span class="post__discussion-unread" v-if="post.is_unread > 0">новых: {{post.is_unread}}</span>
             </div>
          </router-link>
        </div>
        <div class="post__options" v-if="user.id === post.author.id || user.is_staff">
          <v-icon class="post__icon post__delete-icon" @click="deletePost(post)">mdi-delete</v-icon>
        </div>
      </div>
    </div>
  </v-container>
</template>

<script>
import twemoji from 'twemoji'

export default {
  name: 'ForumPost',
  props: ['post', 'type', 'threadStarter'],
  computed: {
    user () {
      return this.$store.getters.getCurrentUser
    },
    currentBranch () {
      return this.$store.getters.getCurrentBranch
    },
    currentThread () {
      return this.$store.getters.getCurrentThread
    },
    currentForum () {
      return this.$store.getters.getCurrentForum
    },
    postClass () {
      return 'post-' + this.post.id
    },
    postTextClass () {
      return 'post-' + this.post.id + '-text'
    }
  },
  methods: {
    deletePost (post) {
      if (this.type === 'post') {
        this.$store.dispatch('deletePost', post)
      } else if (this.type === 'thread') {
        this.$store.dispatch('deleteThread', post)
      }
      if (this.user.id === post.author.id) {
        this.user.messages_count--
        this.user.carma -= post.carma
        const threads = this.$store.getters.getCurrentBranchChildren
        const posts = this.$store.getters.getCurrentThreadChildren
        const allPosts = posts.concat(threads)
        allPosts.push(this.currentThread)
        allPosts.forEach(postInAllPosts => {
          if (postInAllPosts.author.id === post.author.id) {
            postInAllPosts.author.carma = this.user.carma
          }
        })
      }
    },
    likePost (post) {
      const threads = this.$store.getters.getCurrentBranchChildren
      const posts = this.$store.getters.getCurrentThreadChildren
      const allPosts = posts.concat(threads)
      allPosts.push(this.currentThread)
      if (post.users_liked_list.indexOf(this.user.id) === -1) {
        if (this.type === 'post' && !this.threadStarter) {
          this.$store.dispatch('likePost', post)
        } else {
          this.$store.dispatch('likeThread', post)
        }
        if (post.users_disliked_list.indexOf(this.user.id) === -1) {
          allPosts.forEach(postInAllPosts => {
            if (postInAllPosts.author.id === post.author.id) {
              postInAllPosts.author.carma++
            }
            if (postInAllPosts.id === post.id && postInAllPosts.pub_date === post.pub_date) {
              postInAllPosts.users_liked_list.push(this.user.id)
              postInAllPosts.carma++
            }
          })
        } else {
          allPosts.forEach(postInAllPosts => {
            if (postInAllPosts.author.id === post.author.id) {
              postInAllPosts.author.carma++
            }
            if (postInAllPosts.id === post.id && postInAllPosts.pub_date === post.pub_date) {
              postInAllPosts.carma++
              const index = postInAllPosts.users_disliked_list.indexOf(this.user.id)
              postInAllPosts.users_disliked_list.splice(index, 1)
            }
          })
        }
      }
    },
    dislikePost (post) {
      const threads = this.$store.getters.getCurrentBranchChildren
      const posts = this.$store.getters.getCurrentThreadChildren
      const allPosts = posts.concat(threads)
      allPosts.push(this.currentThread)
      if (post.users_disliked_list.indexOf(this.user.id) === -1) {
        if (this.type === 'post' && !this.threadStarter) {
          this.$store.dispatch('dislikePost', post)
        } else {
          this.$store.dispatch('dislikeThread', post)
        }
        if (post.users_liked_list.indexOf(this.user.id) === -1) {
          allPosts.forEach(postInAllPosts => {
            if (postInAllPosts.author.id === post.author.id) {
              postInAllPosts.author.carma--
            }
            if (postInAllPosts.id === post.id && postInAllPosts.pub_date === post.pub_date) {
              postInAllPosts.users_disliked_list.push(this.user.id)
              postInAllPosts.carma--
            }
          })
        } else {
          allPosts.forEach(postInAllPosts => {
            if (postInAllPosts.author.id === post.author.id) {
              postInAllPosts.author.carma--
            }
            if (postInAllPosts.id === post.id && postInAllPosts.pub_date === post.pub_date) {
              postInAllPosts.carma--
              const index = postInAllPosts.users_liked_list.indexOf(this.user.id)
              postInAllPosts.users_liked_list.splice(index, 1)
            }
          })
        }
      }
    },
    clearUnread (post) {
      post.is_unread = 0
    },
    setBranchInPrimary (status) {
      this.$store.dispatch('setBranchInPrimary', status)
    },
    dateRefactor (date) {
      const options = {
        year: 'numeric',
        month: 'numeric',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric'
      }
      date = new Date(date)
      return date.toLocaleString('ru', options)
    },
    async emojiHandler () {
      async function emojiParser (post) {
        await twemoji.parse(post)
      }
      document.getElementsByClassName(this.postClass).forEach(post => emojiParser(post))
      document.getElementsByClassName('emoji').forEach(emoji => {
        emoji.style.cssText = `
          height: 1em;
          width: 1em;
          margin: 0 .05em 0 .1em;
          vertical-align: -0.1em;
        `
      })
    },
    updateAndMountedHandler () {
      document.getElementsByClassName(this.postTextClass).forEach(post => {
        post.innerHTML = this.post.text
      })
      this.emojiHandler()
    }
  },
  updated () {
    this.updateAndMountedHandler()
  },
  mounted () {
    this.updateAndMountedHandler()
  }
}
</script>

<style scoped lang="scss">
@import "../../styles/variables";
.post {
  display: flex;
  min-height: $post__min-height;
  padding: 0;
  margin-top: $post__margin-top;
  flex-direction: row;
}

.post__left-side {
  width: $post__avatar-area__size;
  padding: calc((#{$post__avatar-area__size} - #{$post__avatar__size}) / 2);
  display: flex;
  flex-direction: column;
}

.post__avatar {
  overflow: hidden;
  border-radius: 6px;
  height: $post__avatar__size;
  width: $post__avatar__size;
  border: $third-party solid 1px;
  background-color: white;
}

.post__user_rating {
  color: $third-party;
  text-align: center;
  font-size: 10px;
}

.post__rating_options {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  margin-top: -3px;
}

.post__rating_icon {
  display: flex;
  flex-direction: row;
  justify-content: center;
}

.post__rating_icon i {
  font-size: 16px;
  cursor: pointer;
  transition: 0.2s;
}

.post__rating_icon i:hover {
  transform: scale(1.2);
}

.disabled_icon i {
  cursor: auto;
  color: $third-party;
}

.disabled_icon i:hover {
  transform: none;
}

.rating_minus i:hover  {
  color: $error;
}

.rating_plus i:hover  {
  color: $success
}

.rating_disliked i {
  color: $error;
  transition: none;
  transform: scale(1.2);
}

.rating_liked i {
  color: $success;
  transition: none;
  transform: scale(1.2);
}

.post__post_rating {
  font-size: 12px;
  color: $primary;
  font-weight: 500;
}

.post__right-side {
  width: calc(100% - #{$post__avatar-area__size});
}

.post__header {
  display: flex;
  flex-direction: row;
  align-items: flex-end;
  justify-content: space-between;
  min-height: $post__header__min-height;
}

.post__author {
  font-weight: bold;
  font-size: 14px;
}

.post__pub-date {
  margin-right: $post__padding;
  font-size: 12px;
}

.post__divider {
  width: 100%;
  height: 1px;
  display: flex;
  flex-direction: row;
}

.post__divider-part1 {
  background-color: $third-party;
  width: calc(100% - 7rem);
  height: 100%;
}

.post__divider-part2 {
  background-color: $extra;
  width: 7rem;
  height: 100%;
}

.post__body {
  min-height: calc(#{$post__min-height} - #{$post__header__min-height} - #{$post__footer__min-height});
  padding-left: $post__padding;
}

.post__text {
  white-space: pre-wrap;
  text-align: justify;
  padding-right: 2em;
  word-wrap: break-word;
  width: auto;
}

.post__footer {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  min-height: $post__footer__min-height;
  padding-left: $post__padding;
}

.post__likes-button {
  padding-left: calc(#{$post__padding} / 2);
  cursor: pointer;
}
.post__likes-button__selected {
  color: $extra;
}
.post__discussion a {
  text-decoration: none;
  font-size: 12px;

}
.post__discussion span {
  margin-right: 1rem;
}
.post__discussion-link:hover {
  color: $extra;
  transition: 0.2s;
}
.post__discussion-unread {
  color: $extra;
}
.post__icon {
  font-size: 16px;
  margin-left: 0.2rem;
  margin-right: 0.3rem;
  top: -0.5rem;
}
.post__icon:hover {
  cursor: pointer;
  transform: scale(1.2);
}
.post__delete-icon:hover {
  color: $error;
}
</style>

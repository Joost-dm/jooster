<template>
  <v-container fluid class="post" :class="postClass">
    <div class="post__left-side">
      <v-avatar class="post__avatar">
        <v-img :src=post.author.avatar></v-img>
      </v-avatar>
      <span class="post__user_rating">{{post.author.carma}}</span>
      <div class="post__rating_options">
        <div class="post__rating_icon rating_minus">
          <v-icon>mdi-minus</v-icon>
        </div>
        <span class="post__post_rating">{{post.carma}}</span>
        <div class="post__rating_icon rating_plus">
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
      <div class="post__body">
        <hr>
        <p class="post__text" :class="postTextClass">{{post.text}}</p>
      </div>
      <div class="post__footer">
        <div class="post__likes">
          <span class="post__likes-counter">{{post.likes.length}}</span>
          <span class="post__likes-button mr-5" @click="toggleLikePost(post)">
            <v-icon class="post__likes-button__selected" size="17" v-if="post.likes.indexOf(user.id) != -1">mdi-thumb-up</v-icon>
            <v-icon size="17" v-else >mdi-thumb-up</v-icon>
          </span>
        </div>
        <div class="post__discussion">
          <router-link
            v-if="type === 'thread'"
            :to="{
            name: 'Forum',
            params: {
              forumId: currentForum.id,
              branchId: currentBranch.id,
              threadId: post.id
            }}">
             <div @click="setBranchInPrimary(false)">
               <span>{{post.children_count}}</span>
               <v-icon size="19">mdi-chat</v-icon>
               Непрочитанных: {{post.is_unread}}
             </div>
          </router-link>
        </div>
      </div>
    </div>
  </v-container>
</template>

<script>
import twemoji from 'twemoji'

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
    },
    toggleLikePost (post) {
      if (post.likes.indexOf(this.$store.getters.getCurrentUser.id) === -1) {
        if (this.type === 'post') {
          this.$store.dispatch('likePost', post)
        } else if (this.type === 'thread') {
          this.$store.dispatch('likeThread', post)
        }
        this.post.likes.push(this.user.id)
      } else {
        if (this.type === 'post') {
          this.$store.dispatch('dislikePost', post)
        } else if (this.type === 'thread') {
          this.$store.dispatch('dislikeThread', post)
        }
        for (var i = this.post.likes.length - 1; i >= 0; i--) {
          if (this.post.likes[i] === this.user.id) {
            this.post.likes.splice(i, 1)
          }
        }
      }
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
.rating_minus i:hover  {
  color: $error;
}
.rating_plus i:hover  {
  color: $success
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
  align-items: center;
  min-height: $post__header__min-height;
  padding-left: $post__padding;

}
.post__author {
  font-weight: bold;
}
.post__pub-date {
  margin-left: $post__padding;
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
  align-items: center;
  min-height: $post__footer__min-height;
  padding-left: $post__padding;
}
.post__like {

}
.post__likes-counter {
}
.post__likes-button {
  padding-left: calc(#{$post__padding} / 2);
  cursor: pointer;
}
.post__likes-button__selected {
  color: $extra;
}
.post__discussion a {
  font-weight: bold;
  text-decoration: none;
}
</style>

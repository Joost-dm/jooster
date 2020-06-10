<template>
<v-container fluid class="post" :id="postID">
  <div class="post__left-side">
    <v-avatar class="post__avatar">
      <v-img :src=post.author.avatar></v-img>
    </v-avatar>
  </div>
  <div class="post__right-side">
    <div class="post__header">
      <div class="post__author">
        <span>{{post.author.username}}</span>
      </div>
      <div class="post__pub-date">
        <span>{{dateRefactor(post.pub_date)}}</span>
      </div>
    </div>
    <div class="post__body">
      <hr>
      <pre class="post__text">{{post.text}}</pre>
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
  <!--
<v-container class="pa-0" mb-5>
  <v-img height="50" width="50" v-if="post.author.avatar" :src="post.author.avatar" alt=""></v-img>
  Автор: {{post.author.username}}
  <hr>
  <div style="height: 150px; background-color: gainsboro"><b>{{post.text}}</b></div>
  <hr>
  <span>likes: {{post.likes.length}}</span>
  <br>
  <v-btn @click="toggleLikePost(post)">like</v-btn>
  <v-btn v-if="user.id === post.author.id" @click="deletePost(post)">удалить</v-btn>
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
-->
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
    postID () {
      return 'post-' + this.post.id
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
      await twemoji.parse(document.getElementById(this.postID))
      const emojiList = document.getElementsByClassName('emoji')
      emojiList.forEach(emoji => {
        emoji.style.cssText = `
          height: 1em;
          width: 1em;
          margin: 0 .05em 0 .1em;
          vertical-align: -0.1em;
        `
      })
    }
  },
  mounted () {
    this.emojiHandler()
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
}
.post__avatar {
  overflow: hidden;
  border-radius: 6px;
  height: $post__avatar__size;
  width: $post__avatar__size;
  background-color: white;
}
.post__right-side {
  width: 100%;
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
  font-family: OpenSansEmoji;
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

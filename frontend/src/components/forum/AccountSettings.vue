<template>
  <div class="account_settings">
    <div class="account_settings__window_top">
      <div class="account_settings__user_info">
        <div v-if="previewImageSrc" class="account_settings__user_avatar">
          <img :src="previewImageSrc" alt="">
        </div>
        <div v-else class="account_settings__user_avatar">
          <img :src="user.avatar_url" alt="">
        </div>
        <div>
          <div class="account_settings__user_displayed">
            <p>{{user.displayed}}</p>
          </div>
          <div class="account_settings__user_messages">
            <p>Сообщений: {{user.messages_count}}</p>
          </div>
          <div class="account_settings__user_carma">
            <p>Репутация: {{user.carma}}</p>
          </div>
        </div>
      </div>
      <div class="account_settings__top_controls">
        <v-icon class="account_settings__icon" @click="setAvatar">mdi-content-save</v-icon>
        <v-icon class="account_settings__icon" @click="closeAccountSettings">mdi-chevron-up</v-icon>
      </div>
    </div>

      <v-file-input
        class="account_settings__avatar_input_field"
        id="avatar-input"
        color="black"
        prepend-icon="mdi-camera"
        @change="loadImage"
        accept="image/*"
        show-size
        counter
        label="Изменить аватар"
        requierd
      ></v-file-input>
  </div>
</template>

<script>

export default {
  name: 'AccountSettings',
  data () {
    return {
      UpdatedProfile: null,
      previewImage: null,
      previewImageSrc: null
    }
  },
  computed: {
    user () {
      return this.$store.getters.getCurrentUser
    },
    threads () {
      return this.$store.getters.getCurrentBranchChildren
    },
    posts () {
      return this.$store.getters.getCurrentThreadChildren
    }
  },
  created () {
    this.UpdatedProfile = this.user
  },
  methods: {
    async setAvatar () {
      await this.$store.dispatch('updateUser', this.UpdatedProfile)
      var threads = this.$store.getters.getCurrentBranchChildren
      var posts = this.$store.getters.getCurrentThreadChildren
      var allPosts = posts.concat(threads)
      allPosts.push(this.currentThread)
      allPosts.forEach(post => {
        try {
          if (post.author.id === this.user.id) {
            post.author.avatar_url = this.previewImageSrc
          }
        } catch (error) {
          if (error instanceof TypeError) {
            error.code = 200
          }
        }
      })
      this.user.avatar_url = this.previewImageSrc
      this.$store.dispatch('setAccountSettingsWindowStatus', false)
      delete this.UpdatedProfile.avatar
    },
    loadImage () {
      const target = document.getElementById('avatar-input')
      const file = target.files[0]
      const reader = new FileReader()
      reader.onload = e => {
        this.previewImageSrc = reader.result
      }
      reader.readAsDataURL(file)
      this.UpdatedProfile.avatar = file
    },
    closeAccountSettings () {
      this.$store.dispatch('setAccountSettingsWindowStatus', false)
    }
  }
}
</script>

<style scoped lang="scss">
@import 'src/styles/variables';

.account_settings {
  display: flex;
  flex-direction: column;
  position: absolute;
  background-color: $secondary;
  border: $third-party solid 1px;
  border-radius: 0 0 5px 0;
  width: 500px;
  height: 200px;
  top: -200px;
  z-index: 7;
  transition: 0.5s;
  overflow: hidden;
  padding: calc(#{$navigation-app-bar-height} + 10px) 10px 10px 10px;
  box-shadow:  0 0 5px $shadow
}
.account_settings__window_top {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  justify-content: space-between;
  width: 100%;
}
.account_settings__icon {
  transition: 0.2s;
  padding-left: 5px;
}
.account_settings__icon:hover {
  color: $extra;
}
.account_settings__user_info {
  display: flex;
  flex-direction: row;
  align-items: center;
  margin-left: 10px;
  font-size: 12px;
}
.account_settings__user_info p {
  margin: 0;
}
.account_settings__user_avatar {
  height: $post__avatar__size;
  width: $post__avatar__size;
  border-radius: 5px;
  border: $third-party solid 1px;
  margin-right: 10px;
  overflow: hidden;
  position: relative;
}
.account_settings__user_avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.account_settings__user_displayed {
  font-weight: bold;

  font-size: 15px;
}
.account_settings__avatar_input_field {
  width: 90%;
  font-size: 12px;
}
.account_settings__avatar_input_field .v-icon:hover {
  color: $extra;
}
@media screen and (max-width: 595px){
  .account_settings {
    width: 100%;
    border-radius: 0 0 5px 5px;
  }
}
</style>

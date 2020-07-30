<template>
  <v-container fluid>
    <img alt="preview" v-if="previewImageSrc" class="profile_settings__avatar_preview" :src="previewImageSrc">
    <img v-else class="profile_settings__avatar_preview" :src="user.avatar_url" alt="">
    <v-file-input
                id="avatar-input"
                color="black"
                prepend-icon="mdi-camera"
                @change="loadImage"
                accept="image/*"
                show-size
                counter
                label="Фотография"
                requierd
    ></v-file-input>
    <v-btn @click="setAvatar">set</v-btn>
  </v-container>
</template>

<script>

export default {
  name: 'TrainingView',
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
      this.$router.go(-1)
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
    }
  }
}
</script>
<style scoped>
  .profile_settings__avatar_preview  {
    max-height: 100px !important;
  }
</style>

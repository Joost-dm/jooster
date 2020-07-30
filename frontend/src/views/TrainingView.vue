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
    }
  },
  created () {
    this.UpdatedProfile = this.user
  },
  methods: {
    async setAvatar () {
      this.$store.dispatch('updateUser', this.UpdatedProfile)
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

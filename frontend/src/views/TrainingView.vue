<template>
  <v-container fluid>
    {{user}}
    <v-file-input v-model="UpdatedProfile.avatar">
      avatar
    </v-file-input>
    <v-btn @click="setAvatar">set</v-btn>
  </v-container>
</template>

<script>

export default {
  name: 'TrainingView',
  data () {
    return {
      UpdatedProfile: null
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
    }
  }
}
</script>

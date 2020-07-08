<template>
  <v-btn @click="loginGoogle">Login</v-btn>
</template>

<script>
export default {
  name: 'TrainingVue',
  methods: {
    loginGoogle () {
      this.$store.dispatch('loginGoogle')
    }
  }
}
</script>

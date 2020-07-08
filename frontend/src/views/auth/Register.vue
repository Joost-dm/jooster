<template>
  <div id="main">
    <v-text-field v-model="registerData.username" label="Login"></v-text-field>
    <v-text-field v-model="registerData.email" label="E-mail" type="email"></v-text-field>
    <v-text-field v-model="registerData.password" label="Password" type="password"></v-text-field>
    <v-text-field v-model="password_check" label="Repeat password" type="password"></v-text-field>
    <v-btn @click="createUser">Создать</v-btn>
  </div>
</template>

<script>
export default {
  name: 'Register',
  data () {
    return {
      password_check: '',
      registerData: {
        email: '',
        username: '',
        password: ''
      }
    }
  },
  methods: {
    async createUser () {
      this.registerData.displayed = this.registerData.username
      await this.$store.dispatch('createNewUser', this.registerData)
    }
  },
  computed: {
  }
}
</script>

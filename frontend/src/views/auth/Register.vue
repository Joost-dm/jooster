<template>
  <div id="main">
    <v-form id="register-form" @submit="createUser" enctype="multipart/form-data">
      <v-text-field v-model="registerData.username" label="Login"></v-text-field>
      <v-text-field v-model="registerData.email" label="E-mail" type="email"></v-text-field>
      <v-text-field v-model="registerData.password" label="Password" type="password"></v-text-field>
      <v-text-field v-model="password_check" label="Repeat password" type="password"></v-text-field>
      <v-file-input show-size v-model="registerData.avatar"></v-file-input>
      <v-btn type="submit">Регистрация</v-btn>
    </v-form>
  </div>
</template>

<script>
export default {
  name: 'Register',
  data () {
    return {
      password_check: '',
      registerData: {
        username: '',
        email: '',
        password: '',
        avatar: null
      }
    }
  },
  methods: {
    async createUser () {
      this.$store.dispatch('createNewUser', this.registerData)
    }
  },
  computed: {
  }
}
</script>

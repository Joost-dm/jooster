<template>

  <div id="main">
    <v-form
    ref="form"
    >
      <v-text-field
        v-model="loginData.username"
        label="Login"
        :counter="15"
        required
      />
      <v-text-field
        v-model="loginData.password"
        label="Password"
        type="password"
        :counter="20"
        required
      />
      <v-btn @click="createToken">Войти</v-btn>
      <v-btn @click="destroyToken">Удалить токен</v-btn>
      <v-btn v-if="user" @click="logout">Выйти</v-btn>
      <v-btn @click="loginGoogle">Google</v-btn>
      <br><br>
      <v-divider></v-divider>
      <br><br>
      <span> Токен: {{this.token}}</span>
    </v-form>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data () {
    return {
      loginData: {
        username: '',
        password: ''
      }
    }
  },
  computed: {
    token () {
      return this.$store.getters.getAuthToken
    },
    user () {
      return this.$store.getters.getCurrentUser
    }
  },
  methods: {
    logout () {
      this.$store.dispatch('logoutUser', this.loginData)
    },
    createToken () {
      this.$store.dispatch('loginUser', this.loginData)
    },
    destroyToken () {
      this.$store.dispatch('destroyAuthToken')
    },
    loginGoogle () {
      this.$store.dispatch('loginGoogle')
    }
  }
}
</script>

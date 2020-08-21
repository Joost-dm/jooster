<template>

  <div class="login">
    <div class="login__content">
      <div class="login__header">
        <div class="login__header-title">
          <span>Авторизация</span>
        </div>
      </div>
      <div class="login__form">
        <v-text-field
          v-model="loginData.username"
          label="Имя пользователя"
          :counter="15"
          required
        />
        <v-text-field
          v-model="loginData.password"
          label="Пароль"
          type="password"
          :counter="20"
          required
        />
        <v-btn @click="createToken">Войти</v-btn>
        <v-btn @click="loginGoogle">Google</v-btn>
      </div>
    </div>
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
<style scoped lang="scss">
@import 'src/styles/variables';

.login {
  background-color: $primary;
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.login__content {
  width: 100%;
  max-width: 800px;
  min-width: 300px;
  overflow: hidden;
  border-radius: 10px 10px 0 0;
}
.login__header {
  height: 60px;
  width: 100%;
  background-color: $primary-dark;
  display: flex;
  align-items: center;
}
.login__header-title {
  color: $secondary;
  margin-left: 1rem;
}
.login__form {
  background-color: $secondary;
  padding: 1rem;
}

</style>

<template>
  <div class="login">
    <div class="login__animation-bg1"></div>
    <div class="login__animation-bg1 login__animation-bg2"></div>
    <div class="login__animation-bg1 login__animation-bg3"></div>
    <div  class="login__content">
      <div class="login__header">
        <div class="login__header-title">
          <span v-if="!registration">Авторизация</span>
          <span v-else-if="registration">Регистрация</span>
        </div>
      </div>
      <div class="login__body">
        <v-form v-if="!registration" class="login__login-form">
          <v-text-field
            v-model="username"
            prepend-icon="mdi-account"
            label="Логин"
            required
          />
          <v-text-field
            v-model="password"
            prepend-icon="mdi-lock"
            label="Пароль"
            type="password"
            required
          />
        </v-form>
        <v-form
          v-else-if="registration"
          class="login__register-form"
          ref="form"
          v-model="valid"

          :lazy-validation="lazy">
          <v-text-field
            v-model="username"
            prepend-icon="mdi-account"
            label="Логин"
            :counter="20"
            required
            :rules="loginRules"
          />
          <v-text-field
            v-model="password"
            prepend-icon="mdi-lock"
            label="Пароль"
            type="password"
            required
            :rules="passwordRules"
          />
          <v-text-field
            v-model="retryPassword"
            prepend-icon="mdi-lock-question"
            label="Введите пароль повторно"
            type="password"
            required
            :rules="password_repeatRules"
          />
           <v-text-field
            v-model="name"
            prepend-icon="mdi-smart-card"
            label="Имя"
            :counter="20"
            required
            :rules="nameRules"
          />
          <v-text-field
            v-model="surname"
            prepend-icon="mdi-smart-card"
            label="Фамилия"
            :counter="20"
            required
            :rules="surnameRules"
          />
          <v-text-field
            v-model="email"
            prepend-icon="mdi-email"
            label="E-mail"
            type="email"
            required
            :rules="emailRules"
          />
        </v-form>
        <div class="login__buttons">
          <div class="login__buttons-left-side">
            <v-btn
              small
              v-if="!registration"
              @click="createToken">Войти
            </v-btn>
            <v-btn
              v-if="registration"
              small
              @click="createUser"
              class="login__buttons-button"
              :disabled="!valid || loading"
              :loading="loading">Создать
            </v-btn>
            <v-btn
              @click="loginGoogle"
              small
              class="d-none d-sm-flex login__buttons-button">с помощью Google
            </v-btn>
            <v-btn
              @click="loginGoogle"
              small
              class="d-flex d-sm-none login__buttons-button">Google
            </v-btn>
          </div>
          <div class="login__buttons-right-side">
            <v-btn
              small
              v-if="!registration"
              class="login__buttons-button"
              @click="registration =! registration">Регистрация
            </v-btn>
            <v-btn
              small
              v-if="registration"
              class="login__buttons-button"
              @click="registration =! registration">Отмена
            </v-btn>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data () {
    return {
      registration: false,
      valid: true,
      loading: false,
      username: '',
      password: '',
      retryPassword: '',
      email: '',
      name: '',
      surname: '',
      loginRules: [
        v => !!v || 'Введите логин',
        v => v.length <= 20 || 'Длинна не должна превышать 20 символов',
        v => /^[A-Za-z]([.A-Za-z0-9-]{1,18})([A-Za-z0-9])$/.test(v) || 'Логин должен состоять из латинских букв,' +
          ' цифр, символов "-", ".", и начинаться с буквы. '
      ],
      passwordRules: [
        v => !!v || 'Введите пароль',
        v => v.length <= 127 || 'Длинна пароля не должна превышать 127 символов',
        v => v.length >= 8 || 'Длинна пароля не должна быть менее 8 символов',
        v => /(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z!@#$%^&*]{8,}/.test(v) || 'Пароль должен содержать ' +
          'маленькие и заглавные буквы латинского алфавита и цифры.'
      ],
      password_repeatRules: [
        v => !!v || 'Введите праоль',
        v => (v && v === this.password) || 'Пароли не соответствуют'
      ],
      nameRules: [
        v => !!v || 'Введите ваше имя',
        v => /^[a-zA-Zа-яА-Я'][a-zA-Zа-яА-Я-' ]+[a-zA-Zа-яА-Я']?$/u.test(v) || 'Имя введено некорректно.',
        v => v.length <= 20 || 'Длинна не должна превышать 20 символов'
      ],
      surnameRules: [
        v => !!v || 'Введите вашу фамилию',
        v => /^[a-zA-Zа-яА-Я'][a-zA-Zа-яА-Я-' ]+[a-zA-Zа-яА-Я']?$/u.test(v) || 'Фамилия введена некорректно.',
        v => (v && v.length <= 20) || 'Длинна не должна превышать 20 символов'
      ],
      emailRules: [
        v => !!v || 'Введите E-mail',
        v => /^((([0-9A-Za-z]{1}[-0-9A-z]{1,}[0-9A-Za-z]{1})|([0-9А-Яа-я]{1}[-0-9А-я]{1,}[0-9А-Яа-я]{1}))@([-A-Za-z]{1,}\.){1,2}[-A-Za-z]{2,})$/u.test(v) || 'Некорректный E-mail'
      ],
      lazy: false
    }
  },
  computed: {
    displayed () {
      return this.name + ' ' + this.surname
    },
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
      this.$store.dispatch('loginUser', { username: this.username, password: this.password })
    },
    async createUser () {
      if (this.$refs.form.validate()) {
        try {
          this.loading = true
          await this.$store.dispatch('createNewUser', {
            username: this.username,
            password: this.password,
            email: this.email,
            displayed: this.displayed
          })
          this.loading = false
        } catch {
          this.loading = false
        }
      }
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
  padding: 5%;
}
.login__content {
  width: 100%;
  max-width: 800px;
  min-width: 300px;
  overflow: hidden;
  border-radius: 10px 10px 0 0;
  z-index: 1;
}
.login__header {
  height:45px;
  width: 100%;
  background-color: $primary-dark;
  display: flex;
  align-items: center;
}
.login__header-title {
  color: $secondary;
  margin-left: 1rem;
}
.login__body {
  background-color: $secondary;
  padding: 1rem;
}
.login__buttons {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  flex-wrap: nowrap;
}
.login__buttons-left-side {
  display: flex;
  flex-direction: row;
}
.login__buttons-button {
  margin-left: 1rem;
}

.login__animation-bg1 {
  animation:slide 3s ease-in-out infinite alternate;
  background-image: linear-gradient(-60deg, $primary-dark, 50%, $secondary 50%);
  bottom:0;
  left:-50%;
  opacity:.5;
  position:fixed;
  right:-50%;
  top:0;
  z-index:0;
}

.login__animation-bg2 {
  animation-direction:alternate-reverse;
  animation-duration:4s;
}

.login__animation-bg3 {
  animation-duration:5s;
}

@keyframes slide {
  0% {
    transform:translateX(-25%);
  }
  100% {
    transform:translateX(25%);
  }
}

</style>

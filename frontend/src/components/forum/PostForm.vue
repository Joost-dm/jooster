<template>
  <v-container fluid class="pa-0">
    <div class="bottom-form__picker">
      <picker-area
        set="twitter"
        v-model="newMessage.text"
        pickerPosition="top"
        :i18n="{
        search    : 'Поиск',
        notfound  : 'Не найдено',
        categories: {
          search   : 'Поиск',
          recent   : 'Часто используемые',
          people   : 'Смайлы и люди',
          nature   : 'Животные и природа',
          foods    : 'Еда и напитки',
          activity : 'Хобби',
          places   : 'Путешествия',
          objects  : 'Предметы',
          symbols  : 'Символы',
          flags    : 'Флаги',
          custom   : 'Другое',
        }}" >
      </picker-area>
      <v-icon class="bottom-form__button" @click="createPost">
        mdi-send
      </v-icon>
    </div>
  </v-container>
</template>

<script>
import PickerArea from 'vue-emoji-mart-picker'

export default {
  name: 'PostForm',
  data () {
    return {
      newMessage: {
        text: null
      }
    }
  },
  components: {
    'picker-area': PickerArea
  },
  props: ['type'],
  computed: {
    currentThread () {
      return this.$store.getters.getCurrentThread
    },
    currentBranch () {
      return this.$store.getters.getCurrentBranch
    }
  },
  methods: {
    createPost () {
      alert('clicked')
      if (this.type === 'post') {
        this.newMessage.parent_thread = this.currentThread.id
        this.$store.dispatch('createPost', this.newMessage)
      } else if (this.type === 'thread') {
        this.newMessage.parent_branch = this.currentBranch.id
        this.$store.dispatch('createThread', this.newMessage)
      }
    }
  },
  // заглушка ошибки, возникающей в сторонней библиотеке (емоджи-пикер).
  errorCaptured (err) {
    if (err.name !== 'TypeError') {
      console.error(err)
    }
    return false
  }
}
</script>

<style scoped>
.bottom-form__picker {
  position: relative;
}
.bottom-form__button {
  color: #F98500;
  position: absolute;
  bottom: 5px;
  right: 5px;
  font-size: 25px;
}

</style>
<style lang="scss">
  @import "../../styles/variables";
.emojipicker-area {
  border: $third-party solid 1px !important;
}
.emojipicker-button {
  bottom: 38px !important;
}
</style>

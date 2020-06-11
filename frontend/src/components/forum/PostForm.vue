<template>
 <v-container fluid class="pa-0">
          <picker-area class="primary-view__bottom-form"
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
   <v-icon :v-if="type === 'thread'" class="bottom-form__button" @click="createThread">mdi-message-arrow-right</v-icon>
   <v-icon :else-if="type === 'post'" class="bottom-form__button" @click="createPost">mdi-message-arrow-right</v-icon>
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
    createThread () {
      this.newMessage.parent_branch = this.currentBranch.id
      this.$store.dispatch('createThread', this.newMessage)
    },
    createPost () {
      this.newMessage.parent_thread = this.currentThread.id
      this.$store.dispatch('createPost', this.newMessage)
    }
  }
}
</script>

<style scoped>
.bottom-form__button {
  color: #F98500;
  position: absolute;
  bottom: 5px;
  font-size: 35px;
}
</style>

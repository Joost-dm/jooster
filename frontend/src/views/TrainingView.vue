<template>
  <div class="text-center">
    <v-btn @click="dialog=true"></v-btn>
    <v-dialog class="v-dialog" v-model="dialog">
      <div class="dialog__content">
        <div class="dialog__header">
          <div class="dialog__title">
            <span>заголовок окна</span>
          </div>
          <v-icon class="dialog__close_icon" @click="dialog=false">mdi-close</v-icon>
        </div>
        <div class="dialog__body">
          <users_list></users_list>
        </div>
      </div>
    </v-dialog>
  </div>
</template>

<script>
import UsersList from '@/components/forum/UsersList'
export default {
  name: 'TrainingView',
  data () {
    return {
      dialog: false
    }
  },
  components: {
    users_list: UsersList
  }
}
</script>

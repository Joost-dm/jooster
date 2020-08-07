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
<style lang="scss">
@import "src/styles/variables";

.v-dialog {
  position: relative;
  max-width: 500px;
  height: 80%;
  background-color: $secondary;
  overflow: hidden;
}

.dialog__content {
  display: flex;
  flex-direction: column;
  align-items: center;
  overflow: hidden;
  height: 100%;
}

.dialog__header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  min-height: 45px;
  width: 100%;
  background-color: $primary;
}

.dialog__title {
  color: $secondary;
  font-size: 15px;
  margin-left: 0.7rem;
}
.dialog__close_icon {
  font-size: 20px !important;
  color: $extra !important;
  cursor: pointer;
  margin-right: 0.7rem;
}
.dialog__close_icon:hover {
  transition: 0.1s;
  transform: scale(1.3);
}
.dialog__body {
  display: flex;
  flex-direction: row;
  justify-content: center;
  width: 100%;
  height: calc(100% - 45px);
  overflow: hidden;

}

</style>

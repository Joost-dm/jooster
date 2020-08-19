<template>
  <v-container fluid class="pa-0">
    <div class="forum-create__form">
      <div class="forum-create__form-top">
        <v-text-field
          counter="20"
          v-model="newForum.title" label="Новый форум">
        </v-text-field>
        <div @click="createForum" class="forum-create__send-button-wrapper" >
          <v-icon class="forum-create__send-button">mdi-send</v-icon>
        </div>
      </div>
      <div class="forum-create__form-bottom"></div>
      <v-checkbox dense v-model="newForum.is_private" hide-details class="forum-create__private-checkbox" label="Приватный"></v-checkbox>
    </div>
      </v-container>
</template>

<script>
export default {
  name: 'ForumCreate',
  data () {
    return {
      newForum: {
        title: null,
        is_private: false
      }
    }
  },
  methods: {
    async createForum () {
      await this.$store.dispatch('createForum', this.newForum)
      this.$store.dispatch('getAllForums')
      this.toggleForumCreateForm()
    },
    toggleForumCreateForm () {
      const createForm = document.getElementsByClassName('forum-drawer-header__create-forum-form')[0]
      if (createForm.style.display === 'none' || !createForm.style.display) {
        createForm.style.display = 'inherit'
      } else {
        createForm.style.display = 'none'
      }
    }
  }
}
</script>

<style>
  .forum-create__private-checkbox label {
      font-size: 10px !important;
    }
</style>
<style scoped lang="scss">
  @import '../../styles/variables';
  .forum-create__form {
    padding: 0 1em 0.5em 1em;
  }
  .forum-create__form-top {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
  }
  .forum-create__send-button-wrapper {
    display: flex;
    align-content: center;
  }
  .forum-create__send-button {
    color: $extra !important;
    font-size: 30px !important;
    margin-left: 5px;
    cursor: pointer;
    transition: 0.2s !important;
  }
  .forum-create__send-button:hover {
    transform: scale(1.2);
  }
  .forum-create__form-bottom {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    margin-bottom: -30px;
    padding-bottom: 0;
  }
  .forum-create__private-checkbox {
  }
</style>

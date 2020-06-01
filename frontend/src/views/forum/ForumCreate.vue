<template>
  <v-container fluid class="pa-0">
    <v-text-field
    v-model="newForum.title" label="title"></v-text-field>
    <v-text-field
    v-model="newForum.description" label="description"></v-text-field>
    <v-btn @click="createForum">Создать</v-btn>
  </v-container>
</template>

<script>
export default {
  name: 'ForumCreate',
  data () {
    return {
      newForum: {
        title: null,
        description: null
      }
    }
  },
  methods: {
    async createForum () {
      await this.$store.dispatch('createForum', this.newForum)
      this.$store.dispatch('getAllForums')
    }
  }
}
</script>

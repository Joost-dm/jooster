<template>
  <div>
    test
  </div>
</template>

<script>
export default {
  name: 'ForumDrawerHeader',
  computed: {
    allForums () {
      return this.$store.getters.getAllForumsList
    },
    currentForum () {
      return this.$store.getters.getCurrentForum
    }
  }
}
</script>

<style scoped>

</style>

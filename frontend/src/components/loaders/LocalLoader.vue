<template>
<v-container class="local-loader">
  <v-layout row>
    <v-flex xs12 class="text-center pt-5" >
      <v-progress-circular
        :size="30"
        :width="3"
        color="#363636"
        indeterminate
      ></v-progress-circular>
    </v-flex>
  </v-layout>
</v-container>
</template>

<script>
export default {
  name: 'LocalLoader'
}
</script>

<style scoped>
  .local-loader {
    height: 100px;
  }
</style>

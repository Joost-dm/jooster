<template>
  <div>
  <div class="test" ref="test">TEST</div>
  <v-btn @click="testmethod">click</v-btn>
  </div>

</template>

<script>
export default {
  name: 'TestComponent'
}
</script>
<style scoped>
.test {
  height: 200px;
  width: 200px;
  background-color: greenyellow;
}
</style>

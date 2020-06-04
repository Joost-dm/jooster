export default async function (newVal, oldVal) {
  this.startingPoints.currentForumId = newVal
  if (newVal && newVal !== oldVal) {
    await this.$store.dispatch('getForumValues', this.startingPoints)
  }
}

<template>
<v-row
  id = "forum"
  no-gutters
>
  <v-col
    lg="7"
    md="6"
    id="forum__primary">
    <topics></topics>
  </v-col>
  <v-col
    lg="5"
    md="6"
    id="forum__secondary"
    class="d-none d-sm-flex d-md-flex ">
    <thread></thread>
  </v-col>
</v-row>
</template>

<script>
import Topics from '../../components/forum/PrimaryView'
import Thread from '../../components/forum/SecondaryView'
// import URLChangingMixin from '../../mixins/forumURLChangingMixin.js'
export default {
  data: () => ({}),
  name: 'Forum',
  components: {
    topics: Topics,
    thread: Thread
  },
  props: ['forumId', 'branchId', 'threadId'],
  computed: {
    startingPoints () {
      return {
        currentForumId: this.forumId,
        currentBranchId: this.branchId,
        currentThreadId: this.threadId
      }
    }
  },
  async created () {
    await this.$store.dispatch('getAllForums')
    this.$store.dispatch('getForumValues', this.startingPoints)
    this.windowResizeHandler()
    window.addEventListener('resize', this.windowResizeHandler)
  },
  methods: {
    windowResizeHandler () {
      if (document.documentElement.clientWidth < 595) {
        this.$store.dispatch('setDoubleViewsMode', false)
      } else {
        this.$store.dispatch('setBranchInPrimary', true)
        this.$store.dispatch('setDoubleViewsMode', true)
      }
    }
  },
  watch: {
    forumId: {
      immediate: true,
      deep: true,
      handler: async function (newVal, oldVal) {
        this.startingPoints.currentForumId = newVal
        if (newVal && newVal !== oldVal) {
          await this.$store.dispatch('getForumValues', this.startingPoints)
        }
      }
    },
    branchId: {
      immediate: true,
      deep: true,
      handler: async function (newVal, oldVal) {
        this.startingPoints.currentBranchId = newVal
        if (newVal && newVal !== oldVal) {
          await this.$store.dispatch('getForumValues', this.startingPoints)
        }
      }
    },
    threadId: {
      immediate: true,
      deep: true,
      handler: async function (newVal, oldVal) {
        this.startingPoints.currentThreadId = newVal
        if (newVal && newVal !== oldVal) {
          await this.$store.dispatch('getForumValues', this.startingPoints)
        }
      }
    }
  }
}
</script>

<style scoped>
#forum {
  height: 100%;
}
#forum__primary {
}
#forum__secondary {
}
</style>

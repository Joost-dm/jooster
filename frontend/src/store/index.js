import Vue from 'vue'
import Vuex from 'vuex'
import common from './modules/common'
import authorization from './modules/authorization'
import forums from './modules/forum/forums'
import branches from './modules/forum/branches'
import topics from './modules/forum/posts'
import threads from './modules/forum/threads'
import forumCondition from './modules/forum/forumCondition'
import elements from '@/store/modules/forum/elements'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    authorization,
    common,
    forumCondition,
    forums,
    branches,
    topics,
    threads,
    elements
  }
})

export default {
  state: {
    branchInPrimary: true,
    doubleViewsMode: true,
    currentForum: null,
    currentBranch: null,
    currentThread: null,
    currentBranchBottomScroll: null,
    currentThreadBottomScroll: null,
    currentBranchScrollStart: true,
    currentThreadScrollStart: true,
    localLoaderHeight: 100
  },
  mutations: {
    setBranchInPrimary (state, status) {
      if (!state.doubleViewsMode) {
        state.branchInPrimary = status
      }
    },
    setDoubleViewsMode (state, status) {
      state.doubleViewsMode = status
    },
    setCurrentForum (state, forum) {
      state.currentForum = forum
    },
    setCurrentBranch (state, branch) {
      state.currentBranch = branch
    },
    setCurrentThread (state, thread) {
      state.currentThread = thread
    },
    setCurrentBranchBottomScroll (state, value) {
      state.currentBranchBottomScroll = value
    },
    setCurrentThreadBottomScroll (state, value) {
      state.currentThreadBottomScroll = value
    },
    setCurrentBranchScrollStart (state, boolean) {
      state.currentBranchScrollStart = boolean
    },
    setCurrentThreadScrollStart (state, boolean) {
      state.currentThreadScrollStart = boolean
    }
  },
  actions: {
    setBranchInPrimary ({ commit }, status) {
      commit('setBranchInPrimary', status)
    },
    setDoubleViewsMode ({ commit }, status) {
      commit('setDoubleViewsMode', status)
    },
    async setCurrentForum ({ commit, dispatch, state }, forum) {
      var currentForumId
      if (state.currentForum) {
        currentForumId = state.currentForum.id
      }
      if (currentForumId !== forum.id) {
        commit('setCurrentForum', forum)
        await dispatch('getForumChildren', forum)
        localStorage.setItem('currentForumId', forum.id)
      }
    },
    async setCurrentBranch ({ commit, dispatch, state }, branch) {
      var currentBranchId
      if (state.currentBranch) {
        currentBranchId = state.currentBranch.id
      }
      if (currentBranchId !== branch.id) {
        commit('setCurrentBranch', branch)
        commit('setBranchChildren', null)
        await dispatch('getBranchChildren', { branch: branch })
        localStorage.setItem('currentBranchId', branch.id)
        commit('setCurrentBranchScrollStart', true)
      }
    },
    async setCurrentThread ({ commit, dispatch, state }, thread) {
      var currentThreadId
      if (state.currentThread) {
        currentThreadId = state.currentThread.id
      }
      if (currentThreadId !== thread.id) {
        commit('setCurrentThread', thread)
        commit('setThreadChildren', null)
        await dispatch('getThreadChildren', { thread: thread })
        localStorage.setItem('currentThreadId', thread.id)
        commit('setCurrentThreadScrollStart', true)
      }
    },
    async getForumValues (
      { commit, dispatch, getters }, payload) {
      var currentForumId = +payload.currentForumId
      var currentBranchId = +payload.currentBranchId
      var currentThreadId = +payload.currentThreadId
      const allForumsList = getters.getAllForumsList
      if (!currentForumId) {
        currentForumId = 1
      }
      if (!allForumsList) {
        return ''
      }
      allForumsList.forEach(async function (forum) {
        if (forum.id === currentForumId) {
          await dispatch('setCurrentForum', forum)
        }
      })
      if (!currentBranchId) {
        return ''
      } else if (currentBranchId) {
        await dispatch('getCurrentBranchById', currentBranchId)
        await dispatch('setCurrentBranch', getters.getCurrentBranch)
      }
      if (!currentThreadId) {
        return ''
      } else if (currentThreadId) {
        await dispatch('getCurrentThreadById', currentThreadId)
        await dispatch('setCurrentThread', getters.getCurrentThread)
      }
    },
    setCurrentBranchBottomScroll ({ commit }, value) {
      commit('setCurrentBranchBottomScroll', value)
    },
    setCurrentThreadBottomScroll ({ commit }, value) {
      commit('setCurrentThreadBottomScroll', value)
    },
    setCurrentBranchScrollStart ({ commit }, boolean) {
      commit('setCurrentBranchScrollStart', boolean)
    },
    setCurrentThreadScrollStart ({ commit }, boolean) {
      commit('setCurrentThreadScrollStart', boolean)
    }
  },
  getters: {
    getBranchInPrimary (state) {
      return state.branchInPrimary
    },
    getDoubleViewsModeStatus (state) {
      return state.doubleViewsMode
    },
    getCurrentForum (state) {
      return state.currentForum
    },
    getCurrentBranch (state) {
      return state.currentBranch
    },
    getCurrentThread (state) {
      return state.currentThread
    },
    getCurrentBranchBottomScroll (state) {
      return state.currentBranchBottomScroll
    },
    getCurrentThreadBottomScroll (state) {
      return state.currentThreadBottomScroll
    },
    getCurrentBranchScrollStart (state) {
      return state.currentBranchScrollStart
    },
    getCurrentThreadScrollStart (state) {
      return state.currentThreadScrollStart
    },
    getLocalLoaderHeight (state) {
      return state.localLoaderHeight
    }
  }
}

export default {
  state: {
    globalLoading: false,
    primaryLoading: false,
    secondaryLoading: false,
    drawer: true,
    error: null
  },
  mutations: {
    setPrimaryLoading (state, payload) {
      state.primaryLoading = payload
    },
    setSecondaryLoading (state, payload) {
      state.secondaryLoading = payload
    },
    setGlobalLoading (state, payload) {
      state.globalLoading = payload
    },
    setError (state, error) {
      state.error = error
    },
    clearError (state) {
      state.error = null
    },
    switchDrawer (state) {
      state.drawer = !state.drawer
    }

  },
  actions: {
    setSecondaryLoading ({ commit }, payload) {
      commit('setSecondaryLoading', payload)
    },
    setPrimaryLoading ({ commit }, payload) {
      commit('setPrimaryLoading', payload)
    },
    setGlobalLoading ({ commit }, payload) {
      commit('setGlobalLoading', payload)
    },
    setError ({ commit }, payload) {
      commit('setError', payload)
    },
    clearError ({ commit }, payload) {
      commit('clearError', payload)
    },
    switchDrawer ({ commit }) {
      commit('switchDrawer')
    }
  },
  getters: {
    primaryLoading (state) {
      return state.primaryLoading
    },
    secondaryLoading (state) {
      return state.secondaryLoading
    },
    error (state) {
      return state.error
    },
    drawerStatus (state) {
      return state.drawer
    },
    globalLoading (state) {
      return state.globalLoading
    }
  }
}

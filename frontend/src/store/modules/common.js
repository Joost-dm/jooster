export default {
  state: {
    loading: false,
    drawer: true,
    error: null
  },
  mutations: {
    setLoading (state, payload) {
      state.loading = payload
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
    setLoading ({ commit }, payload) {
      commit('setLoading', payload)
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
    loading (state) {
      return state.loading
    },
    error (state) {
      return state.error
    },
    drawerStatus (state) {
      return state.drawer
    }
  }
}

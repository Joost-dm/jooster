export default {
  state: {
    createForum: null,
    settingsWindow: null
  },
  mutations: {
    setCreateForum (state, element) {
      state.createForum = element
    },
    setSettingsWindow (state, element) {
      state.settingsWindow = element
    },
    toggleCreateForum (state) {
      if (state.createForum.style.display === 'none' || !state.createForum.style.display) {
        state.createForum.style.display = 'inherit'
      } else {
        state.createForum.style.display = 'none'
      }
    },
    toggleSettingsWindow (state) {
      state.settingsWindow.classList.toggle('account_settings__displayed')
    }
  },
  actions: {
    setSettingsWindow ({ commit }, element) {
      commit('setSettingsWindow', element)
    },
    setCreateForum ({ commit }, element) {
      commit('setCreateForum', element)
    },
    toggleSettingsWindow ({ commit }) {
      commit('toggleSettingsWindow')
    },
    toggleCreateForum ({ commit }) {
      commit('toggleCreateForum')
    }
  },
  getters: {
    getTest (state) {
      return state.testElemet
    }
  }
}

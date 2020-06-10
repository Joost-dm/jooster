import axios from 'axios'
import API from '../APIsettings'
import errorMixin from '../../mixins/APIErrorMixin'

export default {
  state: {
    user: null,
    usersList: null,
    auth_token: null
  },
  mutations: {
    createAuthToken (state, token) {
      state.auth_token = token
      localStorage.setItem('auth_token', token)
      axios.defaults.headers.common.Authorization = 'Token ' + token
      axios.defaults.headers.common['Content-Type'] = 'multipart/form-data'
    },
    loginUser (state, newUser) {
      state.user = newUser
    },
    logoutUser (state) {
      localStorage.removeItem('auth_token')
      state.auth_token = null
      state.user = null
      axios.defaults.headers.common.Authorization = null
    },
    setUsersList (state, usersList) {
      state.usersList = usersList
    }
  },
  actions: {
    async loginUser ({ commit }, payload) {
      commit('clearError')
      try {
        var token = await axios.post(API.URL + 'auth_token/token/login/',
          payload)
        commit('createAuthToken', token.data.auth_token)
        var currentUser = await axios.get(API.URL + 'auth/users/me/')
        commit('loginUser', currentUser.data)
      } catch (error) {
        errorMixin(error, commit)
        throw error
      }
    },
    logoutUser ({ commit }) {
      commit('logoutUser')
    },
    async destroyAuthToken ({ commit }, authToken) {
      commit('clearError')
      try {
        await axios.post(API.URL + 'auth_token/token/logout/',
          {
            auth_token: authToken
          })
        commit('logoutUser')
      } catch (error) {
        errorMixin(error, commit)
        throw error
      }
    },
    async createNewUser ({ commit }, user) {
      commit('clearError')
      try {
        const formData = new FormData()
        for (var key in user) {
          formData.append(key, user[key])
        }
        await axios.post(API.URL + 'auth/users/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        await this.loginUser({
          username: user.username,
          password: user.password
        })
      } catch (error) {
        errorMixin(error, commit)
        throw error
      }
    },
    async updateUser ({ commit }, user) {
      commit('clearError')
      const formData = new FormData()
      for (var key in user) {
        formData.append(key, user[key])
      }
      try {
        await axios.put(API.URL + 'auth/users/me/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        var currentUser = await axios.get(API.URL + 'auth/users/me/')
        commit('loginUser', currentUser.data)
      } catch (error) {
        console.log(error.response)
        errorMixin(error, commit)
        throw error
      }
    },
    async checkForLocalAuthToken ({ commit }) {
      function timeout (ms) {
        return new Promise(resolve => setTimeout(resolve, ms))
      }
      commit('clearError')
      if (localStorage.getItem('auth_token')) {
        commit('setGlobalLoading', true)
        const token = localStorage.getItem('auth_token')
        axios.defaults.headers.common.Authorization = 'Token ' + token
        commit('createAuthToken', token)
        await timeout(500)
        try {
          var currentUser = await axios.get(API.URL + 'auth/users/me/')
          commit('loginUser', currentUser.data)
          commit('setGlobalLoading', false)
        } catch (error) {
          commit('setGlobalLoading', false)
          commit('setError', error)
          throw error
        }
      }
    },
    async getUsersList ({ commit }) {
      commit('clearError')
      try {
        var usersList = await axios.get(API.URL + 'auth/users/')
        commit('setUsersList', usersList.data)
        commit('setLoading', false)
      } catch (error) {
        errorMixin(error, commit)
        throw error
      }
    }
  },
  getters: {
    getAuthToken (state) {
      return state.auth_token
    },
    getCurrentUser (state) {
      return state.user
    },
    getUsersList (state) {
      return state.usersList
    }
  }
}

import axios from 'axios'
import router from '../../router'
import API from '../APIsettings'
import errorMixin from '../../mixins/APIErrorMixin'
import firebase from 'firebase/app'
import 'firebase/auth'

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
    },
    updateUser (state, updatedUser) {
      state.user = updatedUser
    }
  },
  actions: {
    async loginUser ({ commit }, payload) {
      commit('clearError')
      try {
        var token = await axios.post(API.URL + 'api/v1/auth_token/token/login/',
          payload)
        commit('createAuthToken', token.data.auth_token)
        var currentUser = await axios.get(API.URL + 'api/v1/auth/users/me/')
        commit('loginUser', currentUser.data)
        commit('setCurrentForum', null)
        router.push('/forum/1/1')
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
        await axios.post(API.URL + 'api/v1/auth_token/token/logout/',
          {
            auth_token: authToken
          })
        commit('logoutUser')
      } catch (error) {
        errorMixin(error, commit)
        throw error
      }
    },
    async createNewUser ({ commit, dispatch }, user) {
      commit('clearError')
      try {
        await axios.post(API.URL + 'api/v1/auth/users/', user)
        await dispatch('loginUser', {
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
        await axios.put(API.URL + 'api/v1/auth/users/me/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        var currentUser = await axios.get(API.URL + 'api/v1/auth/users/me/')
        commit('loginUser', currentUser.data)
      } catch (error) {
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
          var currentUser = await axios.get(API.URL + 'api/v1/auth/users/me/')
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
        var usersList = await axios.get(API.URL + 'api/v1/auth/users/')
        commit('setUsersList', usersList.data)
      } catch (error) {
        errorMixin(error, commit)
        throw error
      }
    },
    async loginGoogle ({ commit, dispatch }) {
      commit('clearError')
      commit('setGlobalLoading', true)
      var provider = new firebase.auth.GoogleAuthProvider()
      const result = await firebase.auth().signInWithPopup(provider)
      const uid = result.user.uid
      const password = result.user.uid.split('').reverse().join('p')
      const displayed = result.user.displayName
      const email = result.user.email
      const photoURL = result.user.photoURL
      try {
        await axios.post(API.URL + 'api/v1/auth/users/', {
          email,
          displayed,
          username: uid,
          password: password,
          foreign_avatar_url: photoURL
        })
      } catch (error) {
        console.log('already exist')
      }
      try {
        await dispatch('loginUser', {
          username: uid,
          password: password
        })
        commit('setGlobalLoading', false)
      } catch (error) {
        errorMixin(error, commit)
        commit('setGlobalLoading', false)
        throw error
      }
    },
    updateUserProfile ({ commit }, updatedUser) {
      commit('updateUser', updatedUser)
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

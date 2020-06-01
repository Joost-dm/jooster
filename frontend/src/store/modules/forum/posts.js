import axios from 'axios'
import API from '../../APIsettings'
import errorMixin from '../../../mixins/APIErrorMixin'

export default {
  state: {
    allPostsList: null
  },
  mutations: {
    getAllThreads (state, allThreadsList) {
      state.allThreadsList = allThreadsList
    }
  },
  actions: {
    async getAllPosts ({ commit }) {
      commit('clearError')
      commit('setLoading', true)
      try {
        const allPostsList = (await axios.get(API.URL + 'api/v1/post/all/')).data
        commit('getAllPosts', allPostsList)
        commit('setLoading', false)
      } catch (error) {
        errorMixin(error, commit)
        commit('setLoading', false)
        throw error
      }
    },
    async createPost ({ commit, dispatch, getters }, post) {
      commit('clearError')
      commit('setLoading', true)
      try {
        await axios.post(API.URL + 'api/v1/post/add/', post)
        commit('setThreadChildren', null)
        await dispatch('getThreadChildren', { thread: getters.getCurrentThread })
        commit('setLoading', false)
      } catch (error) {
        errorMixin(error, commit)
        commit('setLoading', false)
        throw error
      }
    },
    async editPost ({ commit, dispatch, getters }, post) {
      commit('clearError')
      commit('setLoading', true)
      try {
        await axios.put(API.URL + 'api/v1/post/' + post.id + '/', post)
        commit('setThreadChildren', null)
        await dispatch('getThreadChildren', { thread: getters.getCurrentThread })
        commit('setLoading', false)
      } catch (error) {
        errorMixin(error, commit)
        commit('setLoading', false)
        throw error
      }
    },
    async deletePost ({ commit, dispatch, getters }, post) {
      commit('clearError')
      commit('setLoading', true)
      try {
        await axios.delete(API.URL + 'api/v1/post/' + post.id + '/')
        commit('setThreadChildren', null)
        await dispatch('getThreadChildren', { thread: getters.getCurrentThread })
        commit('setLoading', false)
      } catch (error) {
        errorMixin(error, commit)
        commit('setLoading', false)
        throw error
      }
    },
    async likePost ({ commit, dispatch, getters }, post) {
      commit('clearError')
      try {
        await axios.post(API.URL + 'api/v1/post/' + post.id + '/like/')
      } catch (error) {
        errorMixin(error, commit)
      }
    },
    async dislikePost ({ commit, dispatch, getters }, post) {
      commit('clearError')
      try {
        await axios.delete(API.URL + 'api/v1/post/' + post.id + '/like/')
      } catch (error) {
        errorMixin(error, commit)
      }
    }
  },
  getters: {
    getAllPostsList (state) {
      return state.allPostsList
    }
  }
}

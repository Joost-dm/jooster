import axios from 'axios'
import API from '../../APIsettings'
import errorMixin from '../../../mixins/APIErrorMixin'

export default {
  state: {
    allForumsList: null,
    currentForumChildrenList: null
  },
  mutations: {
    getAllForums (state, allForumsList) {
      state.allForumsList = allForumsList
    },
    getForumChildren (state, childrenList) {
      state.currentForumChildrenList = childrenList
    }
  },
  actions: {
    async getAllForums ({ commit }) {
      commit('clearError')
      commit('setLoading', true)
      try {
        const allForumsList = (await axios.get(API.URL + 'api/v1/forum/all/')).data
        commit('getAllForums', allForumsList)
        commit('setLoading', false)
      } catch (error) {
        errorMixin(error, commit)
        commit('setLoading', false)
        throw error
      }
    },
    async getCurrentForumById ({ commit, dispatch }, id) {
      commit('clearError')
      commit('setLoading', true)
      try {
        const currentForum = (await axios.get(API.URL + 'api/v1/forum/' + id + '/')).data
        await dispatch('setCurrentForum', currentForum)
        commit('setLoading', false)
      } catch (error) {
        errorMixin(error, commit)
        commit('setLoading', false)
        throw error
      }
    },
    async createForum ({ commit }, forum) {
      commit('clearError')
      commit('setLoading', true)
      try {
        await axios.post(API.URL + 'api/v1/forum/add/', forum)
        commit('setLoading', false)
      } catch (error) {
        errorMixin(error, commit)
        commit('setLoading', false)
        throw error
      }
    },
    async editForum ({ commit }, forum) {
      commit('clearError')
      commit('setLoading', true)
      try {
        await axios.put(API.URL + 'api/v1/forum/' + forum.id + '/', forum)
        commit('setLoading', false)
      } catch (error) {
        errorMixin(error, commit)
        commit('setLoading', false)
        throw error
      }
    },
    async deleteForum ({ commit, dispatch }, forum) {
      commit('clearError')
      commit('setLoading', true)
      try {
        await axios.delete(API.URL + 'api/v1/forum/' + forum.id + '/')
        await dispatch('getAllForums')
        commit('setLoading', false)
      } catch (error) {
        errorMixin(error, commit)
        commit('setLoading', false)
        throw error
      }
    },
    async getForumChildren ({ commit }, forum) {
      commit('clearError')
      commit('setLoading', true)
      try {
        const childrenList = await axios.get(API.URL + 'api/v1/forum/' + forum.id + '/children/')
        commit('getForumChildren', childrenList.data)
        commit('setLoading', false)
      } catch (error) {
        errorMixin(error, commit)
        commit('setLoading', false)
        throw error
      }
    },
    async addForumMember ({ commit }, payload) {
      commit('clearError')
      commit('setLoading', true)
      try {
        await axios.post(API.URL + 'api/v1/forum/' + payload.forum.id + '/membership/' + payload.user.id + '/')
        commit('setLoading', false)
      } catch (error) {
        errorMixin(error, commit)
        commit('setLoading', false)
        throw error
      }
    }
  },
  getters: {
    getAllForumsList (state) {
      return state.allForumsList
    },
    getCurrentForumChildren (state) {
      return state.currentForumChildrenList
    }
  }
}

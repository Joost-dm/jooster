import axios from 'axios'
import API from '../../APIsettings'
import errorMixin from '../../../mixins/APIErrorMixin'

export default {
  state: {
    allThreadsList: null,
    currentThreadChildrenList: [],
    threadNextPageUrl: null,
    threadPreviousPageUrl: null
  },
  mutations: {
    setAllThreads (state, allThreadsList) {
      state.allThreadsList = allThreadsList
    },
    setThreadChildren (state, childrenList) {
      if (!childrenList) {
        state.currentThreadChildrenList = []
      } else {
        state.currentThreadChildrenList = childrenList.concat(state.currentThreadChildrenList)
      }
    },
    setThreadNextPageUrl (state, url) {
      state.threadNextPageUrl = url
    },
    setThreadPreviousPageUrl (state, url) {
      state.threadPreviousPageUrl = url
    }
  },
  actions: {
    async getAllThreads ({ commit }) {
      commit('clearError')
      commit('setLoading', true)
      try {
        const allThreadsList = (await axios.get(API.URL + 'api/v1/thread/all/')).data
        commit('setAllThreads', allThreadsList)
        commit('setLoading', false)
      } catch (error) {
        errorMixin(error, commit)
        commit('setLoading', false)
        throw error
      }
    },
    async getCurrentThreadById ({ commit, dispatch }, id) {
      commit('clearError')
      commit('setLoading', true)
      try {
        const currentThread = (await axios.get(API.URL + 'api/v1/thread/' + id + '/')).data
        await dispatch('setCurrentThread', currentThread)
        commit('setLoading', false)
      } catch (error) {
        errorMixin(error, commit)
        commit('setLoading', false)
        throw error
      }
    },
    async createThread ({ commit, dispatch, getters }, thread) {
      commit('clearError')
      commit('setLoading', true)
      try {
        await axios.post(API.URL + 'api/v1/thread/add/', thread)
        commit('setBranchChildren', null)
        await dispatch('getBranchChildren', { branch: getters.getCurrentBranch })
        commit('setLoading', false)
      } catch (error) {
        errorMixin(error, commit)
        commit('setLoading', false)
        throw error
      }
    },
    async editThread ({ commit }, thread, dispatch, getters) {
      commit('clearError')
      commit('setLoading', true)
      try {
        await axios.put(API.URL + 'api/v1/thread/' + thread.id + '/', thread)
        commit('setBranchChildren', null)
        await dispatch('getBranchChildren', { branch: getters.getCurrentBranch })
        commit('setLoading', false)
      } catch (error) {
        errorMixin(error, commit)
        commit('setLoading', false)
        throw error
      }
    },
    async deleteThread ({ commit, dispatch, getters }, thread) {
      commit('clearError')
      commit('setLoading', true)
      try {
        await axios.delete(API.URL + 'api/v1/thread/' + thread.id + '/')
        commit('setBranchChildren', null)
        await dispatch('getBranchChildren', { branch: getters.getCurrentBranch })
        commit('setLoading', false)
      } catch (error) {
        errorMixin(error, commit)
        commit('setLoading', false)
        throw error
      }
    },
    async getThreadChildren ({ commit, dispatch }, payload, state, getters) {
      var url
      if (!payload.url) {
        url = API.URL + 'api/v1/thread/' + payload.thread.id + '/children/'
      } else {
        url = payload.url
        dispatch('setCurrentThreadScrollStart', false)
      }
      commit('clearError')
      commit('setLoading', true)
      try {
        const childrenList = await axios.get(url)
        if (childrenList.data.next) {
          commit('setThreadNextPageUrl', childrenList.data.next)
        } else {
          commit('setThreadNextPageUrl', null)
        }
        if (childrenList.data.previous) {
          commit('setThreadPreviousPageUrl', childrenList.data.previous)
        } else {
          commit('setThreadPreviousPageUrl', null)
          dispatch('setCurrentThreadBottomScroll', 0)
        }
        const reversedChildrenList = childrenList.data.results.reverse()
        commit('setThreadChildren', reversedChildrenList)
        commit('setLoading', false)
      } catch (error) {
        errorMixin(error, commit)
        commit('setLoading', false)
        throw error
      }
    },
    async likeThread ({ commit, dispatch, getters }, thread) {
      commit('clearError')
      try {
        await axios.post(API.URL + 'api/v1/thread/' + thread.id + '/like/')
      } catch (error) {
        errorMixin(error, commit)
      }
    },
    async dislikeThread ({ commit, dispatch, getters }, thread) {
      commit('clearError')
      try {
        await axios.delete(API.URL + 'api/v1/thread/' + thread.id + '/like/')
      } catch (error) {
        errorMixin(error, commit)
      }
    }
  },
  getters: {
    getAllThreadsList (state) {
      return state.allThreadsList
    },
    getCurrentThreadChildren (state) {
      return state.currentThreadChildrenList
    },
    getThreadNextPageUrl (state) {
      return state.threadNextPageUrl
    },
    getThreadPreviousPageUrl (state) {
      return state.threadPreviousPageUrl
    }
  }
}

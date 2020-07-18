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
      try {
        const allThreadsList = (await axios.get(API.URL + 'api/v1/thread/all/')).data
        commit('setAllThreads', allThreadsList)
      } catch (error) {
        errorMixin(error, commit)
        throw error
      }
    },
    async getCurrentThreadById ({ commit, dispatch }, id) {
      commit('clearError')
      try {
        const currentThread = (await axios.get(API.URL + 'api/v1/thread/' + id + '/')).data
        await dispatch('setCurrentThread', currentThread)
      } catch (error) {
        errorMixin(error, commit)
        throw error
      }
    },
    async createThread ({ commit, dispatch, getters }, thread) {
      commit('clearError')
      try {
        await axios.post(API.URL + 'api/v1/thread/add/', thread)
        commit('setBranchChildren', null)
        await dispatch('getBranchChildren', { branch: getters.getCurrentBranch })
      } catch (error) {
        errorMixin(error, commit)
        throw error
      }
    },
    async editThread ({ commit }, thread, dispatch, getters) {
      commit('clearError')
      try {
        await axios.put(API.URL + 'api/v1/thread/' + thread.id + '/', thread)
        commit('setBranchChildren', null)
        await dispatch('getBranchChildren', { branch: getters.getCurrentBranch })
      } catch (error) {
        errorMixin(error, commit)
        throw error
      }
    },
    async deleteThread ({ commit, dispatch, getters }, thread) {
      commit('clearError')
      try {
        await axios.delete(API.URL + 'api/v1/thread/' + thread.id + '/')
        commit('setBranchChildren', null)
        await dispatch('getBranchChildren', { branch: getters.getCurrentBranch })
      } catch (error) {
        errorMixin(error, commit)
        throw error
      }
    },
    async getThreadChildren ({ commit, dispatch, getters }, payload) {
      function timeout (ms) {
        return new Promise(resolve => setTimeout(resolve, ms))
      }
      if (getters.getBranchInPrimary) {
        commit('setSecondaryLoading', true)
      } else {
        commit('setPrimaryLoading', true)
      }
      await timeout(1500)
      var url
      if (!payload.url) {
        url = API.URL + 'api/v1/thread/' + payload.thread.id + '/children/'
      } else {
        url = payload.url
        dispatch('setCurrentThreadScrollStart', false)
      }
      commit('clearError')
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
        getters.getBranchInPrimary ? commit('setSecondaryLoading', false) : commit('setPrimaryLoading', false)
      } catch (error) {
        errorMixin(error, commit)
        getters.getBranchInPrimary ? commit('setSecondaryLoading', false) : commit('setPrimaryLoading', false)
        throw error
      }
    },
    async likeThread ({ commit, dispatch, getters }, thread) {
      commit('clearError')
      try {
        await axios.post(API.URL + 'api/v1/thread/' + thread.id + '/like/', { like: true })
      } catch (error) {
        errorMixin(error, commit)
      }
    },
    async dislikeThread ({ commit, dispatch, getters }, thread) {
      commit('clearError')
      try {
        await axios.delete(API.URL + 'api/v1/thread/' + thread.id + '/like/', { like: false })
      } catch (error) {
        errorMixin(error, commit)
      }
    },
    clearThreadChildren ({ commit }) {
      commit('setThreadChildren')
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

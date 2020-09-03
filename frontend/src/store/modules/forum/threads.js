import axios from 'axios'
import API from '../../../../APIsettings'
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
        commit('setCurrentBranchBottomScroll', 0)
        const currentBranchChildren = getters.getCurrentBranchChildren
        commit('setBranchChildren', null)
        commit('setBranchChildren', currentBranchChildren)
        await dispatch('getBranchChildren', { branch: getters.getCurrentBranch, lazy: true })
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
        var currentBranchChildren = getters.getCurrentBranchChildren
        for (var i = 0; i < currentBranchChildren.length; i++) {
          if (currentBranchChildren[i].id === thread.id) {
            currentBranchChildren.splice(i, 1)
          }
        }
        commit('setBranchChildren', null)
        commit('setBranchChildren', currentBranchChildren)
        if (thread.id === getters.getCurrentThread.id) {
          commit('setCurrentThread', null)
        }
      } catch (error) {
        errorMixin(error, commit)
        throw error
      }
    },
    async getThreadChildren ({ commit, dispatch, getters }, payload) {
      if (getters.getBranchInPrimary && !payload.lazy) {
        commit('setSecondaryLoading', true)
      } else if (!payload.lazy) {
        commit('setPrimaryLoading', true)
      }
      var url
      if (!payload.url) {
        url = API.URL + 'api/v1/thread/' + payload.thread.id + '/children/'
      } else {
        url = API.URL + payload.url.split(':')[2].substr(5)
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
        if (payload.lazy) {
          commit('setThreadChildren', null)
          dispatch('setCurrentThreadBottomScroll', 0)
        }
        commit('setThreadChildren', reversedChildrenList)
        getters.getBranchInPrimary ? commit('setSecondaryLoading', false) : commit('setPrimaryLoading', false)
      } catch (error) {
        commit('setSecondaryLoading', false)
        commit('setPrimaryLoading', false)
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
        if (error.code !== 304) {
          errorMixin(error, commit)
        }
      }
    },
    async dislikeThread ({ commit, dispatch, getters }, thread) {
      commit('clearError')
      try {
        await axios.post(API.URL + 'api/v1/thread/' + thread.id + '/like/', { like: false })
      } catch (error) {
        if (error.code !== 304) {
          errorMixin(error, commit)
        }
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

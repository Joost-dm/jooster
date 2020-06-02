import axios from 'axios'
import API from '../../APIsettings'
import errorMixin from '../../../mixins/APIErrorMixin'

export default {
  state: {
    allBranchesList: null,
    currentBranchChildrenList: [],
    branchNextPageUrl: null,
    branchPreviousPageUrl: null
  },
  mutations: {
    setAllBranches (state, allBranchesList) {
      state.allBranchesList = allBranchesList
    },
    setBranchChildren (state, childrenList) {
      if (!childrenList) {
        state.currentBranchChildrenList = []
      } else {
        state.currentBranchChildrenList = childrenList.concat(state.currentBranchChildrenList)
      }
    },
    setBranchNextPageUrl (state, url) {
      state.branchNextPageUrl = url
    },
    setBranchPreviousPageUrl (state, url) {
      state.branchPreviousPageUrl = url
    }
  },
  actions: {
    async getAllBranches ({ commit }) {
      commit('clearError')
      commit('setLoading', true)
      try {
        const allBranchesList = (await axios.get(API.URL + 'api/v1/branch/all/')).data
        commit('setAllBranches', allBranchesList)
        commit('setLoading', false)
      } catch (error) {
        errorMixin(error, commit)
        commit('setLoading', false)
        throw error
      }
    },
    async getCurrentBranchById ({ commit, dispatch }, id) {
      commit('clearError')
      commit('setLoading', true)
      try {
        const currentBranch = (await axios.get(API.URL + 'api/v1/branch/' + id + '/')).data
        await dispatch('setCurrentBranch', currentBranch)
        commit('setLoading', false)
      } catch (error) {
        errorMixin(error, commit)
        commit('setLoading', false)
        throw error
      }
    },
    async createBranch ({ commit }, branch) {
      commit('clearError')
      commit('setLoading', true)
      try {
        await axios.post(API.URL + 'api/v1/branch/add/', branch)
        commit('setLoading', false)
      } catch (error) {
        errorMixin(error, commit)
        commit('setLoading', false)
        throw error
      }
    },
    async editBranch ({ commit }, branch) {
      commit('clearError')
      commit('setLoading', true)
      try {
        await axios.put(API.URL + 'api/v1/branch/' + branch.id + '/', branch)
        commit('setLoading', false)
      } catch (error) {
        errorMixin(error, commit)
        commit('setLoading', false)
        throw error
      }
    },
    async deleteBranch ({ commit, dispatch, getters }, branch) {
      commit('clearError')
      commit('setLoading', true)
      try {
        await axios.delete(API.URL + 'api/v1/branch/' + branch.id + '/')
        await dispatch('getForumChildren', getters.getCurrentForum)
        commit('setLoading', false)
      } catch (error) {
        errorMixin(error, commit)
        commit('setLoading', false)
        throw error
      }
    },
    async getBranchChildren ({ commit, dispatch }, payload) {
      var url
      if (payload.url) {
        url = payload.url
        dispatch('setCurrentBranchScrollStart', false)
      } else {
        url = API.URL + 'api/v1/branch/' + payload.branch.id + '/children/'
      }
      commit('clearError')
      commit('setLoading', true)
      try {
        const childrenList = await axios.get(url)
        if (childrenList.data.next) {
          commit('setBranchNextPageUrl', childrenList.data.next)
        } else {
          commit('setBranchNextPageUrl', null)
        }
        if (childrenList.data.previous) {
          commit('setBranchPreviousPageUrl', childrenList.data.previous)
        } else {
          commit('setBranchPreviousPageUrl', null)
          dispatch('setCurrentBranchBottomScroll', 0)
        }
        const reversedChildrenList = childrenList.data.results.reverse()
        commit('setBranchChildren', reversedChildrenList)
        commit('setLoading', false)
      } catch (error) {
        errorMixin(error, commit)
        commit('setLoading', false)
        throw error
      }
    },
    async addBranchMember ({ commit }, payload) {
      commit('clearError')
      commit('setLoading', true)
      try {
        await axios.post(API.URL + 'api/v1/branch/' + payload.branch.id + '/membership/' + payload.user.id + '/')
        commit('setLoading', false)
      } catch (error) {
        errorMixin(error, commit)
        commit('setLoading', false)
        throw error
      }
    }
  },
  getters: {
    getAllBranchesList (state) {
      return state.allBranchesList
    },
    getCurrentBranchChildren (state) {
      return state.currentBranchChildrenList
    },
    getBranchNextPageUrl (state) {
      return state.branchNextPageUrl
    },
    getBranchPreviousPageUrl (state) {
      return state.branchPreviousPageUrl
    }
  }
}

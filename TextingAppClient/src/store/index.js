import { createStore } from 'vuex'

export default createStore({
  state: {
    token: '',
    isAuthenticated: false,
    userId: -1,
  },
  mutations: {
    initializeStore(state) {
      if ( localStorage.getItem('token')) {
        state.token = localStorage.getItem('token')
        state.isAuthenticated = true;
      }
    },
    setToken(state, token, id) {
      state.token = token
      state.isAuthenticated = true
      state.userId = id
    },
    removeToken(state) {
      state.token = ''
      state.isAuthenticated = false
      state.userId = -1;
    }
  },
  actions: {

  },
  modules: {

  }
})
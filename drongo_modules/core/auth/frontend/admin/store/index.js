import axios from 'axios'

export const state = () => ({
  token: null,
  authenticated: false,
  username: null,
  redirectOrigin: null
})

export const mutations = {
  saveToken (state, {token, username}) {
    state.authenticated = true
    state.token = token
    state.username = username
    axios.defaults.headers.common['Authorization'] = token
  },

  revokeToken (state) {
    state.token = null
    state.authenticated = false
    state.username = null
  },

  saveRedirectOrigin (state, redirectOrigin) {
    state.redirectOrigin = redirectOrigin
  },

  removeRedirectOrigin (state) {
    state.redirectOrigin = null
  }
}

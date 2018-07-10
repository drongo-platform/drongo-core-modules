// Register Auth components
import Vue from 'vue'

import ChangePassword from '~auth/components/ChangePassword'
import Login from '~auth/components/Login'
import Register from '~auth/components/Register'
import LoginInfo from '~auth/components/LoginInfo'
import UserSelect from '~auth/components/UserSelect'

Vue.component('d-admin-auth-changepassword', ChangePassword)
Vue.component('d-admin-auth-login', Login)
Vue.component('d-admin-auth-register', Register)
Vue.component('d-admin-auth-logininfo', LoginInfo)
Vue.component('d-admin-auth-userselect', UserSelect)

// Register the auth store
const files = require.context('~auth/store', true, /^\.\/(?!-)[^.]+\.(js)$/)
export default ({store}) => {
  store.registerModule('auth', {
    ...files('./index.js'),
    namespaced: true
  })
}

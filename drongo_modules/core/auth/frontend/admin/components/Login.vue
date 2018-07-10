<template>
  <div class="login">
    <form class="form" v-if="!$store.state.auth.authenticated" method="post" @submit.prevent="login">
      <h3>Login</h3>
      <div v-if="apiErrors._" class="form__errors">
        <p v-for="(msg, index) in apiErrors._" :key="index">{{ msg }}</p>
      </div>
      <div class="form__control" :class="{error: apiErrors.username}">
        <label>Username</label>
        <div v-if="apiErrors.username" class="form__errors">
          <p v-for="(msg, index) in apiErrors.username" :key="index">{{ msg }}</p>
        </div>
        <input type="text" name="username" v-model="form.username" />
      </div>
      <div class="form__control">
        <label>Password</label>
        <div v-if="apiErrors.password" class="form__errors">
          <p v-for="(msg, index) in apiErrors.password" :key="index">{{ msg }}</p>
        </div>
        <input type="password" name="password" v-model="form.password" />
      </div>
      <button type="submit" class="button">Log-in</button>
    </form>
    <div v-else style="text-align: center;">
      Logged in!<br/>
      <a href="#" @click.prevent="logout">Logout</a> or,
      proceed to <nuxt-link to="/">admin</nuxt-link>
    </div>
  </div>
</template>

<script>
  import { mapMutations } from 'vuex'
  import AuthService from '~auth/service'

  export default {
    methods: {
      login () {
        AuthService.login(
          this.form
        ).then(({token}) => {
          this.$cookie.set('AuthToken', token, {expires: '7D'})
          this.$cookie.set('AuthUser', this.form.username, {expires: '7D'})
          this.saveToken({token, username: this.form.username})
          this.$emit('loggedin', {token, username: this.form.username})

          var redirect = this.$store.state.auth.redirectOrigin || '/'
          this.$store.commit('auth/removeRedirectOrigin')
          this.$router.push(redirect)

          // Reset form and errors
          this.apiErrors = {}
          this.form = {username: '', password: ''}
        }).catch(errors => {
          this.apiErrors = errors
        })
      },

      logout () {
        AuthService.logout().then((resp) => {
          this.$cookie.delete('AuthToken')
          this.$cookie.delete('AuthUser')
          this.revokeToken()
          this.$emit('loggedout')
        })
      },

      ...mapMutations({
        saveToken: 'auth/saveToken',
        revokeToken: 'auth/revokeToken'
      })
    },

    data () {
      return {
        apiErrors: {},

        form: {
          username: '',
          password: ''
        }
      }
    }
  }
</script>

<style lang="scss">
  .login {
    background-color: #FFF;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    text-align: left;
    padding: 2rem;
    border-radius: 4px;
    margin: 0 auto;
    max-width: 400px;
    width: 100%;

    // h3 {
    //   color: #AAAAAA;
    //   letter-spacing: 0.1em;
    //   text-align: center;
    //   text-transform: uppercase;
    // }
  }
</style>

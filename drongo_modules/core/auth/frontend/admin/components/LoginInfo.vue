<template>
  <div class="auth-info" v-if="$store.state.auth.authenticated">
    Hello <nuxt-link to="/auth/me">{{ $store.state.auth.username }}</nuxt-link>,
    <a href="#" @click.prevent="logout"><i class="icon-logout"></i></a>
  </div>
  <div class="username" v-else>
    <nuxt-link to="/auth/login">Login</nuxt-link>
  </div>
</template>

<script>
  import AuthService from '~auth/service'

  export default {
    methods: {
      logout () {
        AuthService.logout().then((resp) => {
          this.$store.commit('auth/revokeToken')
          this.$cookie.delete('AuthToken')
          this.$cookie.delete('AuthUser')
          this.$router.push('/auth/login')
        })
      }
    }
  }
</script>

<style lang="scss">
  .auth-info {
    a {
      background-color: #FFFFFF;
      padding: 0.2rem 1rem;
      border-radius: 0.4rem;
    }
  }
</style>

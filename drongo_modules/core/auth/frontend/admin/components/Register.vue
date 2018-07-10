<template>
  <div class="register">
    <div class="form" v-if="!$store.state.auth.authenticated">
      <h3>Register</h3>
      <div v-if="errors.length > 0" class="errors">
        <p v-for="msg in errors">{{ msg }}</p>
      </div>
      <label>Username</label>
      <input type="text" name="username" v-model="form.username" />
      <label>Password</label>
      <input type="password" name="password" v-model="form.password" />
      <button type="submit" class="button" @click.prevent="login">Register</button>
      &nbsp;
      <nuxt-link to="/">Back</nuxt-link>
    </div>
    <div v-else style="text-align: center;">
      Already logged in! <a href="#" @click.prevent="logout">Logout</a>
    </div>
  </div>
</template>

<script>
  // import AuthService from '~auth/service'

  export default {
    methods: {
      login () {
        fetch(`${process.env.apiUrl}/auth/users/`, {
          method: 'POST',
          body: JSON.stringify(this.form),
          headers: new Headers({
            'Content-Type': 'application/json'
          })
        }).then(res => res.json()).then(resp => {
          if (resp.status === 'OK') {
            this.errors = []
            this.$emit('registered')
          } else {
            this.errors = []
            Object.keys(resp.errors).map((key) => {
              resp.errors[key].map((msg) => {
                this.errors.push(msg)
              })
            })
          }
        })
      },

      logout () {
        this.$store.commit('auth/revoke')
      }
    },

    data () {
      return {
        errors: [],
        form: {
          username: '',
          password: ''
        }
      }
    }
  }
</script>

<style lang="scss" scoped>
  .register {
    background-color: #FFF;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    text-align: left;
    padding: 2rem;
    border-radius: 4px;
    margin: 0 auto;
    max-width: 400px;
    width: 100%;

    .errors {
      background-color: #c0392b;
      border-radius: 4px;
      color: #FFFFFF;
      padding: 1rem;
      margin-bottom: 1rem;

      p {
        margin: 0 0 0.2rem;
      }
    }

    h3 {
      color: #AAAAAA;
      letter-spacing: 0.1em;
      text-align: center;
      text-transform: uppercase;
    }
  }
</style>

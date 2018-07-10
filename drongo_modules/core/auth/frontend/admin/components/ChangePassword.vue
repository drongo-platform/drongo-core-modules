<template>
  <form class="form" method="post" @submit.prevent="submit">
    <d-admin-form-password label="Current Password" v-model="password"></d-admin-form-password>
    <d-admin-form-password label="New Password" v-model="newPassword"></d-admin-form-password>
    <d-admin-form-password label="Repeat Password" v-model="repeatPassword"></d-admin-form-password>
    <div v-if="passwordsDontMatch">Passwords do not match!</div>
    <button class="button button--primary">Save</button>
  </form>
</template>

<script>
  import authService from '~auth/service'

  export default {
    methods: {
      submit () {
        if (this.passwordsDontMatch) {
          return
        }

        authService.changePassword(
          {password: this.password, newPassword: this.newPassword}
        ).then((res) => {
          // do nothing
        })
      }
    },

    computed: {
      passwordsDontMatch () {
        return this.newPassword !== this.repeatPassword
      }
    },

    data () {
      return {
        password: '',
        newPassword: '',
        repeatPassword: ''
      }
    }
  }
</script>

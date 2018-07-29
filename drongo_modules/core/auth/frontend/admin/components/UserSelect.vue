<template>
  <div class="form__control">
    <label>{{ label }}</label>
    <!-- <v-select :value="value" @input="updateValue($event)" :options="userList.map((item) => item.username)"></v-select> -->
    <input type="text" :value="value" @input="updateValue($event.target.value)" />
  </div>
</template>

<script>
  import authService from '~auth/service'

  export default {
    props: ['label', 'value'],

    methods: {
      loadUsers () {
        authService.list().then((res) => {
          this.userList = res
        })
      },

      updateValue (newVal) {
        this.$emit('input', newVal)
      }
    },

    mounted () {
      // this.loadUsers()
    },

    data () {
      return {
        userList: []
      }
    }
  }
</script>

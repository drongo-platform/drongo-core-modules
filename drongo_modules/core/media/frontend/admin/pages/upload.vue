<template>
  <div class="page">
    <h2 class="page__title">
      <i class="icon-pencil"></i>
      Media / <small>Upload</small>
    </h2>
    <div class="panel">
      <div class="panel__body">
        <form class="form" method="post" @submit.stop.prevent="submit">
          <input type="file" name="" value="" accept="image/*" @change="filechanged" multiple />
          <button type="submit" class="button button--primary">Upload</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'

  export default {
    methods: {
      filechanged (e) {
        this.files = e.target.files
      },

      submit () {
        let formData = new FormData()
        formData.append('file', this.files[0])
        axios.post(
          `${process.env.apiUrl}/media/admin/public/upload`,
          formData,
          { headers: { 'Content-Type': 'multipart/form-data' } }
        ).then((resp) => {
        })
      }
    },

    data () {
      return {
        files: []
      }
    }
  }
</script>

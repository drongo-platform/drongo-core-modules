import axios from 'axios'

const baseUrl = `${process.env.apiUrl}/media`

export default {
  admin: {
    container: {
      create ({name, description}) {
        return axios.post(
          `${baseUrl}/admin/containers`,
          {name, description}
        )
      },

      get ({name}) {
        return axios.get(
          `${baseUrl}/admin/containers/${name}`
        )
      },

      update ({name, description}) {
        return axios.put(
          `${baseUrl}/admin/containers/${name}`,
          {description}
        )
      },

      delete ({name}) {
        return axios.delete(
          `${baseUrl}/admin/containers/${name}`
        )
      },

      list () {
        return axios.get(
          `${baseUrl}/admin/containers`
        )
      }
    },

    media: {
      upload ({container, files}) {
        let formData = new FormData()
        for (var i = 0; i < files.length; i++) {
          formData.append('file', files[i])
        }
        return axios.post(
          `${baseUrl}/admin/containers/${container}/upload`,
          formData,
          { headers: { 'Content-Type': 'multipart/form-data' } }
        )
      },

      list ({container}) {
        return axios.get(
          `${baseUrl}/admin/containers/${container}/media`
        )
      },

      delete ({container, key}) {
        return axios.delete(
          `${baseUrl}/admin/containers/${container}/media/${key}`
        )
      }
    }
  }
}

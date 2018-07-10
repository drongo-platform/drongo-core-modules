<template>
  <div class="page">
    <h2 class="page__title">
      <i class="icon-pencil"></i>
      Media
    </h2>

    <div class="grid">
      <div class="grid__col grid__col--03">
        <div class="panel">
          <div class="panel__head">
            Containers
          </div>
          <div class="panel__body">
            <table class="table table--type1">
              <thead>
                <tr>
                  <th>Name</th>
                  <th style="width: 10px;"></th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="container in containers" :class="{selected: container == selectedContainer}">
                  <td>
                    <a href="#" @click.prevent="selectContainer(container)">{{ container.name }}</a>
                  </td>
                  <td>
                    <a href="#" class="button button--danger" @click.prevent="deleteContainer(container)"><i class="icon-trash"></i></a>
                  </td>
                </tr>
              </tbody>
            </table>
            <p>&nbsp;</p>
          </div>
        </div>
        <div class="panel">
          <div class="panel__head">Create Container</div>
          <div class="panel__body">
            <form class="form" method="post" @submit.prevent="createContainer">
              <div class="form__control">
                <label>Name</label>
                <input type="text" v-model="newContainer.name" />
              </div>
              <div class="form__control">
                <label>Description</label>
                <textarea type="text" v-model="newContainer.description"></textarea>
              </div>
              <button type="submit" class="button button--primary">Create</button>
            </form>
          </div>
        </div>
      </div>
      <div class="grid__col grid__col--09">
        <div class="panel" v-if="selectedContainer !== null">
          <div class="panel__head">
            Media <small>[{{ selectedContainer.name }}]</small>
          </div>
          <div class="panel__body">
            <div class="media-items" style="max-height: 65vh;">
              <div class="media-items__item-wrap" v-for="item in mediaItems">
                <div class="media-items__item">
                  <div class="media-items__image-wrap" v-if="item.mimetype.startsWith('image/')">
                    <div class="media-items__image" :style="{'background-image': `url('${getMediaUrl(item.url)}')`}">
                      <img :src="`${item.url}`" />
                    </div>
                  </div>
                  <div class="media-items__actions">
                    <a href="#" class="button button--info"><i class="icon-pencil"></i></a>
                    <a href="#" class="button button--danger" @click.prevent="deleteMedia(item.key)"><i class="icon-trash"></i></a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="selectedContainer !== null" class="panel">
          <div class="panel__head">Upload</div>
          <div class="panel__body">
            <form class="form" method="post" @submit.stop.prevent="uploadMedia">
              <d-admin-form-dropzonefile @change="uploadFileChanged"></d-admin-form-dropzonefile>
              <button type="submit" class="button button--primary">Upload</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import services from '~media/service'

  export default {
    data () {
      return {
        containers: [],
        selectedContainer: null,
        mediaItems: [],

        newContainer: {
          name: ''
        },

        upload: {
          files: []
        }
      }
    },

    methods: {
      createContainer () {
        services.admin.container.create({ name: this.newContainer.name }).then(() => {
          this.newContainer.name = ''
          this.loadContainerList()
        })
      },

      loadContainerList () {
        services.admin.container.list().then((resp) => {
          this.containers = resp.data.payload
        })
      },

      selectContainer (container) {
        this.selectedContainer = container
        this.loadMedia()
      },

      deleteContainer (container) {
        if (this.selectedContainer === container) {
          this.selectedContainer = null
        }
        services.admin.container.delete({name: container.name}).then(() => {
          this.loadContainerList()
        })
      },

      loadMedia () {
        services.admin.media.list(
          {container: this.selectedContainer.name}
        ).then((resp) => {
          this.mediaItems = resp.data.payload
        })
      },

      uploadFileChanged (e) {
        this.upload.files = e.target.files
      },

      uploadMedia () {
        services.admin.media.upload({
          container: this.selectedContainer.name,
          files: this.upload.files
        }).then((resp) => {
          this.loadMedia()
        })
      },

      deleteMedia (key) {
        services.admin.media.delete({
          container: this.selectedContainer.name,
          key: key
        }).then((resp) => {
          this.loadMedia()
        })
      },

      getMediaUrl (url) {
        return process.env.apiUrl + '/media' + url
      }
    },

    mounted () {
      this.loadContainerList()
    }
  }
</script>

<style lang="scss">
  @import '~assets/variables';

  .media-items {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: start;
    overflow-y: auto;

    &__item-wrap {
      padding: 1.2rem;
      width: 25%;
    }

    &__item {
      border: #EEE 1px solid;
      border-radius: 0.4rem;
      justify-content: center;
      padding: 1.2rem;
      text-align: center;
    }

    &__image-wrap {
      position: relative;
      padding-bottom: 66%;
    }

    &__image {
      align-items: center;
      background-position: center;
      background-size: cover;
      bottom: 0;
      display: flex;
      flex-direction: column;
      justify-content: center;
      left: 0;
      position: absolute;
      right: 0;
      top: 0;

      img {
        display: none;
        min-width: 100%;
        min-height: 100%;
      }
    }

    &__actions {
      margin-top: 1.2rem;

      a {
        margin: 0 0.4rem;
      }
    }
  }

  tr.selected {
    border-left: $color-primary 4px solid;
  }
</style>

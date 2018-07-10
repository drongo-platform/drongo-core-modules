<template>
  <div class="form__control">
    <label>{{ label }}</label><br />
    <img class="preview" :src="mediaUrl" />
    <input type="text" :value="value" readonly />
    <div class="button-group">
      <a href="#" @click.prevent="state.browserVisible = true" class="button button--info button--small"><i class="icon-list"></i> Browse</a>
      <a href="#" @click.prevent="clear" class="button button--small"><i class="icon-close"></i> Reset</a>
    </div>

    <div class="image-browser" :class="{'image-browser--show': state.browserVisible}">
      <div class="media-items">
        <div class="media-items__item-wrap" v-for="image in images">
          <div class="media-items__item" v-if="image.mimetype.startsWith('image')">
            <div class="media-items__image-wrap" v-if="image.mimetype.startsWith('image/')">
              <div class="media-items__image" :style="{'background-image': `url('${getMediaUrl(image.url)}')`}">
                <img :src="getMediaUrl(image.url)" />
              </div>
            </div>
            <div class="media-items__actions">
              <a href="#" class="button button-primary" @click="selectImage(image)">Select</a>
            </div>
          </div>
        </div>
      </div>
      <div class="image-browser__upload">
        <form class="form" method="post" @submit.stop.prevent="uploadMedia">
          <d-admin-form-dropzonefile @change="uploadFileChanged"></d-admin-form-dropzonefile>
        </form>
      </div>
      <div class="image-browser__buttons">
        <a href="#" @click.prevent="state.browserVisible = false">Cancel</a>
      </div>
    </div>
  </div>
</template>

<script>
  import mediaService from '~media/service'

  export default {
    props: ['label', 'value', 'container'],

    computed: {
      mediaUrl () {
        return this.getMediaUrl(this.value)
      }
    },

    methods: {
      loadImageList () {
        mediaService.admin.media.list({container: this.container}).then((resp) => {
          this.images = resp.data.payload
        })
      },

      selectImage (image) {
        this.$emit('input', image.url)
        this.state.browserVisible = false
      },

      clear () {
        this.$emit('input', '')
      },

      uploadFileChanged (e) {
        mediaService.admin.media.upload({
          container: this.container,
          files: e.target.files
        }).then((resp) => {
          this.loadImageList()
        })
      },

      getMediaUrl (url) {
        return process.env.apiUrl + '/media' + url
      }
    },

    mounted () {
      this.loadImageList()
    },

    data () {
      return {
        state: {
          browserVisible: false
        },

        images: []
      }
    }
  }
</script>

<style lang="scss">
  @import '~assets/variables';

  img.preview {
    margin: 0 auto;
    max-width: 90%;
  }

  .image-browser {
    background-color: #FFFFFF;
    bottom: 1.2rem;
    display: none;
    flex-direction: column;
    left: 1.2rem;
    overflow-y: auto;
    position: fixed;
    right: 1.2rem;
    top: 1.2rem;

    &--show {
      display: block;
      z-index: 999;
    }

    &__buttons {
      bottom: 1.2rem;
      position: fixed;
      left: 1.2rem;
      padding: 1.2rem 2rem;
      right: 1.2rem;
      text-align: right;
    }
  }

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
</style>

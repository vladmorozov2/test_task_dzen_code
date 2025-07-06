<template>
  <div class="comment-form">
    <h2>{{ parentId !== null ? 'Reply to Comment' : 'Add New Comment' }}</h2>

    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="text">Comment*</label>
        <div class="editor-toolbar">
          <button type="button" @click="insertTag('i')" title="Italic"><i>I</i></button>
          <button type="button" @click="insertTag('strong')" title="Bold"><strong>B</strong></button>
          <button type="button" @click="insertTag('code')" title="Code"><code>Code</code></button>
          <button type="button" @click="insertLink" title="Link">🔗</button>
        </div>
        <textarea id="text" v-model="form.text" :class="{ error: errors.text || htmlErrors.length }" rows="5"
          ref="textarea"></textarea>
        <div v-if="errors.text" class="error-message">{{ errors.text }}</div>
        <div v-if="htmlErrors.length" class="error-message">
          <ul>
            <li v-for="(error, index) in htmlErrors" :key="index">{{ error }}</li>
          </ul>
        </div>
      </div>

      <!-- File Upload -->
      <div class="form-group">
        <label>Attachment</label>
        <input type="file" ref="fileInput" @change="handleFileUpload" accept="image/jpeg,image/png,image/gif,.txt" />
        <div v-if="previewImage" class="preview-container">
          <img :src="previewImage" alt="Preview" class="preview-image" @click="openLightbox(previewImage)" />
          <button type="button" @click="removePreview" class="remove-btn">×</button>
        </div>
        <div v-if="fileError" class="error-message">{{ fileError }}</div>
        <div v-if="attachment" class="attachment-info">
          <div v-if="attachment.type === 'text'">
            <div class="file-icon">📄</div>
            <div class="file-name">{{ attachment.name }}</div>
            <div class="file-size">{{ formatFileSize(attachment.size) }}</div>
          </div>
        </div>
      </div>

      <!-- reCAPTCHA -->
      <div class="form-group">
        <div :id="recaptchaContainerId"></div>
        <div v-if="captchaError" class="error-message">{{ captchaError }}</div>
      </div>

      <!-- Preview Button -->
      <div class="form-group">
        <button type="button" @click="togglePreview" class="preview-btn">
          {{ showPreview ? 'Hide Preview' : 'Show Preview' }}
        </button>
      </div>

      <!-- Preview Section -->
      <div v-if="showPreview" class="preview-section">
        <h3>Comment Preview</h3>
        <div class="preview-content">
          <div v-html="renderPreview()"></div>
          <div v-if="previewImage" class="preview-image-container">
            <img :src="previewImage" alt="Preview" @click="openLightbox(previewImage)" />
          </div>
          <div v-if="attachment && attachment.type === 'text'" class="text-preview">
            <div class="file-icon">📄</div>
            <div class="file-info">
              <div class="file-name">{{ attachment.name }}</div>
              <div class="file-size">{{ formatFileSize(attachment.size) }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Submit Button -->
      <div class="form-group">
        <button type="submit" :disabled="isSubmitting" class="submit-btn">
          {{ isSubmitting ? 'Submitting...' : 'Submit Comment' }}
        </button>
      </div>

      <!-- Cancel button for replies -->
      <div v-if="parentId !== null" class="form-group">
        <button type="button" @click="$emit('cancel')" class="cancel-btn">
          Cancel Reply
        </button>
      </div>
    </form>

    <Lightbox v-if="lightboxVisible" :imageUrl="currentImage" @close="lightboxVisible = false" />
  </div>
</template>

<script>
import api from '../axios'
import Lightbox from './Lightbox.vue'

export default {
  name: 'CommentForm',
  components: { Lightbox },
  props: {
    parentId: {
      type: Number,
      default: null,
    },
  },
  data() {
    return {
      form: {
        text: '',
      },
      errors: {},
      htmlErrors: [],
      attachment: null,
      previewImage: null,
      fileError: '',
      showPreview: false,
      isSubmitting: false,
      lightboxVisible: false,
      currentImage: null,
      captchaResponse: null,
      captchaVerified: false,
      captchaError: '',
      recaptchaWidgetId: null,
      recaptchaContainerId: 'recaptcha-container-' + Math.random().toString(36).substr(2, 9),
    }
  },
  mounted() {
    if (window.grecaptcha && window.grecaptcha.render) {
      this.renderRecaptcha()
    } else {
      window.vueRecaptchaOnLoad = () => {
        this.renderRecaptcha()
      }
    }
  },
  methods: {
    renderRecaptcha() {
      if (this.recaptchaWidgetId !== null) return

      this.recaptchaWidgetId = window.grecaptcha.render(this.recaptchaContainerId, {
        sitekey: '6Le_w3krAAAAAPQrQavEf7O4Wfs9kUmJdYYAY7u3',
        callback: this.onCaptchaVerified,
        'expired-callback': this.onCaptchaExpired,
      })
    },

    onCaptchaVerified(token) {
      this.captchaResponse = token
      this.captchaVerified = true
      this.captchaError = ''
    },

    onCaptchaExpired() {
      this.captchaResponse = null
      this.captchaVerified = false
    },

    togglePreview() {
      this.showPreview = !this.showPreview
    },

    validateForm() {
      this.errors = {}
      this.htmlErrors = []

      if (!this.form.text.trim()) {
        this.errors.text = 'Comment text is required.'
      }

      const invalidTags = this.validateHTML(this.form.text)
      if (invalidTags.length) {
        this.htmlErrors = invalidTags
      }

      return Object.keys(this.errors).length === 0 && this.htmlErrors.length === 0
    },

    validateHTML(text) {
      const errors = []
      if (/<script/i.test(text)) {
        errors.push('Script tags are not allowed.')
      }
      return errors
    },

    insertTag(tag) {
      const textarea = this.$refs.textarea
      const start = textarea.selectionStart
      const end = textarea.selectionEnd
      const selected = this.form.text.substring(start, end)
      const before = this.form.text.substring(0, start)
      const after = this.form.text.substring(end)

      this.form.text = before + `<${tag}>` + selected + `</${tag}>` + after

      this.$nextTick(() => {
        textarea.focus()
        textarea.selectionStart = start + tag.length + 2
        textarea.selectionEnd = end + tag.length + 2
      })
    },

    insertLink() {
      const url = prompt('Enter the URL')
      if (!url) return

      const textarea = this.$refs.textarea
      const start = textarea.selectionStart
      const end = textarea.selectionEnd
      const selected = this.form.text.substring(start, end) || 'link text'
      const before = this.form.text.substring(0, start)
      const after = this.form.text.substring(end)

      this.form.text = before + `<a href="${url}">${selected}</a>` + after

      this.$nextTick(() => {
        textarea.focus()
        textarea.selectionStart = start + 9 + url.length
        textarea.selectionEnd = start + 9 + url.length + selected.length
      })
    },

    handleFileUpload(event) {
      this.fileError = ''
      const file = event.target.files[0]
      if (!file) {
        this.attachment = null
        this.previewImage = null
        return
      }

      const validImageTypes = ['image/jpeg', 'image/png', 'image/gif']
      const validTextTypes = ['text/plain']

      if (
        !validImageTypes.includes(file.type) &&
        !validTextTypes.includes(file.type)
      ) {
        this.fileError = 'Unsupported file type. Allowed: jpeg, png, gif, txt.'
        this.attachment = null
        this.previewImage = null
        this.$refs.fileInput.value = ''
        return
      }

      this.attachment = {
        name: file.name,
        size: file.size,
        type: validImageTypes.includes(file.type) ? 'image' : 'text',
      }

      if (this.attachment.type === 'image') {
        const reader = new FileReader()
        reader.onload = e => {
          this.attachment.data = e.target.result
          this.previewImage = e.target.result
        }
        reader.readAsDataURL(file)
      } else {
        this.previewImage = null
      }
    },

    removePreview() {
      this.attachment = null
      this.previewImage = null
      this.fileError = ''
      if (this.$refs.fileInput) this.$refs.fileInput.value = ''
    },

    openLightbox(imageUrl) {
      this.currentImage = imageUrl
      this.lightboxVisible = true
    },

    renderPreview() {
      return this.form.text
    },

    formatFileSize(size) {
      if (size < 1024) return size + ' bytes'
      else if (size < 1024 * 1024)
        return (size / 1024).toFixed(1) + ' KB'
      else return (size / (1024 * 1024)).toFixed(1) + ' MB'
    },

    dataURLtoBlob(dataURL) {
      const byteString = atob(dataURL.split(',')[1])
      const mimeString = dataURL.split(',')[0].split(':')[1].split(';')[0]
      const ab = new ArrayBuffer(byteString.length)
      const ia = new Uint8Array(ab)

      for (let i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i)
      }

      return new Blob([ab], { type: mimeString })
    },

    async submitForm() {
      this.captchaError = ''
      if (!this.captchaVerified) {
        this.captchaError = 'Please verify that you are not a robot.'
        return
      }

      if (!this.validateForm()) return

      this.isSubmitting = true

      try {
        const formData = new FormData()

        formData.append('text', this.form.text)
        if (this.parentId !== null) {
          formData.append('parent_comment', this.parentId)
        }

        if (this.attachment) {
          if (this.attachment.type === 'image') {
            const blob = this.dataURLtoBlob(this.attachment.data)
            formData.append('attachment', blob, this.attachment.name)
          } else {
            const fileInput = this.$refs.fileInput
            if (fileInput.files.length > 0) {
              formData.append('attachment', fileInput.files[0])
            }
          }
        }

        formData.append('captcha', this.captchaResponse)

        await api.post('/api/comments/', formData)

        this.resetForm()
        this.$emit('submitted')

        if (this.recaptchaWidgetId !== null) {
          window.grecaptcha.reset(this.recaptchaWidgetId)
        }
        this.captchaResponse = null
        this.captchaVerified = false
      } catch (error) {
        if (error.response && error.response.data.errors) {
          this.errors = error.response.data.errors
        } else {
          console.error('Error submitting comment:', error)
          this.errors.text = 'Error submitting comment. Please try again.'
        }
      } finally {
        this.isSubmitting = false
      }
    },

    resetForm() {
      this.form = { text: '' }
      this.removePreview()
      this.showPreview = false
      this.htmlErrors = []
      this.errors = {}
    },
  },
}
</script>
<style scoped>
.comment-form {
  background-color: #ffffff;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  margin-bottom: 40px;
  border: 1px solid #eaeaea;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.comment-form:hover {
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.12);
  transform: translateY(-3px);
}

.comment-form h2 {
  color: #2c3e50;
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 1px solid #f0f0f0;
  font-size: 1.8rem;
}

.form-group {
  margin-bottom: 25px;
  position: relative;
}

label {
  display: block;
  margin-bottom: 10px;
  font-weight: 600;
  color: #34495e;
  font-size: 1rem;
}

input[type="text"],
input[type="email"],
input[type="url"],
textarea {
  width: 100%;
  padding: 14px 16px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background-color: #fafafa;
}

input[type="text"]:focus,
input[type="email"]:focus,
input[type="url"]:focus,
textarea:focus {
  border-color: #3498db;
  outline: none;
  box-shadow: 0 0 0 4px rgba(52, 152, 219, 0.15);
  background-color: #ffffff;
}

input[type="text"].error,
input[type="email"].error,
textarea.error {
  border-color: #e74c3c;
}

input::placeholder {
  color: #95a5a6;
}

textarea {
  min-height: 150px;
  resize: vertical;
  line-height: 1.6;
}

.editor-toolbar {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.editor-toolbar button {
  background: #ecf0f1;
  border: 1px solid #d6dbdf;
  border-radius: 6px;
  padding: 8px 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 5px;
}

.editor-toolbar button:hover {
  background: #d6dbdf;
  transform: translateY(-2px);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.preview-btn {
  background: #95a5a6;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 10px 18px;
  cursor: pointer;
  margin-bottom: 15px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.preview-btn:hover {
  background: #7f8c8d;
  transform: translateY(-2px);
}

.preview-section {
  border: 1px solid #eaeaea;
  border-radius: 8px;
  padding: 20px;
  margin-top: 20px;
  background-color: #f9f9f9;
  animation: fadeIn 0.4s ease;
}

.preview-section h3 {
  margin-top: 0;
  color: #2c3e50;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
  margin-bottom: 15px;
}

.preview-content {
  padding: 15px;
  background: white;
  border-radius: 6px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03);
}

.submit-btn {
  background: #2ecc71;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 14px 28px;
  cursor: pointer;
  font-size: 1.1rem;
  font-weight: 600;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.submit-btn:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
  transform: none !important;
}

.submit-btn:not(:disabled):hover {
  background: #27ae60;
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(46, 204, 113, 0.3);
}

.error-message {
  color: #e74c3c;
  font-size: 0.9rem;
  margin-top: 8px;
  font-weight: 500;
}

.error-message ul {
  margin: 5px 0;
  padding-left: 20px;
}

.error-message li {
  margin-bottom: 3px;
}

.preview-container {
  position: relative;
  display: inline-block;
  margin-top: 15px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  cursor: pointer;
}

.preview-image {
  max-width: 100%;
  max-height: 200px;
  display: block;
  transition: transform 0.3s ease;
}

.preview-image:hover {
  transform: scale(1.03);
}

.remove-btn {
  position: absolute;
  top: -10px;
  right: -10px;
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 50%;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 18px;
  font-weight: bold;
  transition: all 0.3s ease;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.remove-btn:hover {
  background: #c0392b;
  transform: rotate(90deg) scale(1.1);
}

.attachment-info {
  margin-top: 10px;
  padding: 10px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background: #f8f9fa;
}

.file-icon {
  font-size: 24px;
  margin-right: 10px;
}

.file-name {
  font-weight: bold;
  margin-bottom: 5px;
}

.file-size {
  font-size: 0.85rem;
  color: #666;
}

.text-preview {
  display: flex;
  align-items: center;
  padding: 10px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background: #f8f9fa;
  margin-top: 10px;
}

.file-info {
  margin-left: 10px;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .comment-form {
    padding: 20px;
  }

  .editor-toolbar {
    flex-wrap: wrap;
  }

  .submit-btn {
    width: 100%;
    padding: 16px;
  }
}
</style>
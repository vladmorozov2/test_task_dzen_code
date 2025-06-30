<template>
  <div class="comment-form">
    <h2>{{ parentId !== null ? 'Reply to Comment' : 'Add New Comment' }}</h2>

    <form @submit.prevent="submitForm">
      <!-- Username Field -->
      <div class="form-group">
        <label for="username">Username*</label>
        <input
          type="text"
          id="username"
          v-model="form.username"
          :class="{ error: errors.username }"
        />
        <div v-if="errors.username" class="error-message">{{ errors.username }}</div>
      </div>

      <!-- Email Field -->
      <div class="form-group">
        <label for="email">Email*</label>
        <input
          type="email"
          id="email"
          v-model="form.email"
          :class="{ error: errors.email }"
        />
        <div v-if="errors.email" class="error-message">{{ errors.email }}</div>
      </div>

      <!-- Homepage Field -->
      <div class="form-group">
        <label for="homepage">Homepage</label>
        <input
          type="url"
          id="homepage"
          v-model="form.homepage"
          placeholder="https://example.com"
        />
      </div>

      <!-- Text Editor -->
      <div class="form-group">
        <label for="text">Comment*</label>
        <div class="editor-toolbar">
          <button type="button" @click="insertTag('i')" title="Italic"><i>I</i></button>
          <button type="button" @click="insertTag('strong')" title="Bold"><strong>B</strong></button>
          <button type="button" @click="insertTag('code')" title="Code"><code>Code</code></button>
          <button type="button" @click="insertLink" title="Link">🔗</button>
        </div>
        <textarea
          id="text"
          v-model="form.text"
          :class="{ error: errors.text }"
          rows="5"
        ></textarea>
        <div v-if="errors.text" class="error-message">{{ errors.text }}</div>
      </div>

      <!-- File Upload -->
      <div class="form-group">
        <label>Attachment123</label>
        <input
          type="file"
          ref="fileInput"
          @change="handleFileUpload"
          accept="image/jpeg,image/png,image/gif,.txt"
        />
        <div v-if="previewImage" class="preview-container">
          <img :src="previewImage" alt="Preview" class="preview-image" />
          <button type="button" @click="removePreview" class="remove-btn">×</button>
        </div>
        <div v-if="fileError" class="error-message">{{ fileError }}</div>
      </div>
      <div>
        <AttachmentPreview>
          
        </AttachmentPreview>
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
            <img :src="previewImage" alt="Preview" />
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
  </div>
</template>

<script>
import api from '../axios'
import AttachmentPreview from './AttachmentPreview.vue'

export default {
  name: 'CommentForm',
  props: {
    parentId: {
      type: Number,
      default: null
    }
  },
  data() {
    return {
      form: {
        username: '',
        email: '',
        homepage: '',
        text: ''
      },
      errors: {},
      file: null,
      previewImage: null,
      fileError: '',
      showPreview: false,
      isSubmitting: false
    }
  },
  methods: {
    handleFileUpload(event) {
      const file = event.target.files[0]
      if (!file) return

      const validImageTypes = ['image/jpeg', 'image/png', 'image/gif']
      const maxImageSize = 100 * 1024 // 100KB

      if (validImageTypes.includes(file.type)) {
        if (file.size > maxImageSize) {
          this.fileError = 'Image size exceeds 100KB limit'
          return
        }
        const reader = new FileReader()
        reader.onload = (e) => {
          this.previewImage = e.target.result
          this.file = file
          this.fileError = ''
        }
        reader.readAsDataURL(file)
      } else if (file.type === 'text/plain' || file.name.endsWith('.txt')) {
        if (file.size > 100 * 1024) {
          this.fileError = 'Text file size exceeds 100KB limit'
          return
        }
        this.file = file
        this.fileError = ''
      } else {
        this.fileError = 'Invalid file type. Only JPG, PNG, GIF, or TXT allowed'
      }
    },
    removePreview() {
      this.previewImage = null
      this.file = null
      this.$refs.fileInput.value = ''
    },
    insertTag(tag) {
      const textarea = document.getElementById('text')
      const start = textarea.selectionStart
      const end = textarea.selectionEnd
      const selectedText = this.form.text.substring(start, end)

      let newText = ''
      if (tag === 'a') {
        newText = `<a href="${this.form.homepage || 'https://example.com'}" title="">${selectedText || 'link'}</a>`
      } else {
        newText = `<${tag}>${selectedText || tag}</${tag}>`
      }

      this.form.text =
        this.form.text.substring(0, start) +
        newText +
        this.form.text.substring(end)

      setTimeout(() => {
        textarea.selectionStart = start + newText.length
        textarea.selectionEnd = start + newText.length
        textarea.focus()
      }, 0)
    },
    insertLink() {
      this.insertTag('a')
    },
    togglePreview() {
      this.showPreview = !this.showPreview
    },
    renderPreview() {
      return this.form.text
    },
    validateForm() {
      this.errors = {}
      let isValid = true

      if (!this.form.username) {
        this.errors.username = 'Username is required'
        isValid = false
      } else if (!/^[a-zA-Z0-9]+$/.test(this.form.username)) {
        this.errors.username = 'Only Latin letters and numbers allowed'
        isValid = false
      }

      if (!this.form.email) {
        this.errors.email = 'Email is required'
        isValid = false
      } else if (!/\S+@\S+\.\S+/.test(this.form.email)) {
        this.errors.email = 'Invalid email format'
        isValid = false
      }

      if (
        this.form.homepage &&
        !/^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/.test(
          this.form.homepage
        )
      ) {
        this.errors.homepage = 'Invalid URL format'
        isValid = false
      }

      if (!this.form.text) {
        this.errors.text = 'Comment text is required'
        isValid = false
      }

      return isValid
    },
    async submitForm() {
      if (!this.validateForm()) return

      this.isSubmitting = true

      try {
        const formData = new FormData()
        formData.append('username', this.form.username)
        formData.append('email', this.form.email)
        formData.append('homepage', this.form.homepage)
        formData.append('text', this.form.text)
        formData.append('sender', 1)
        formData.append('sender_id', 1)


        if (this.parentId !== null) {
          formData.append('parent_comment', this.parentId)
        }

        if (this.file) {
          formData.append('attachment', this.file)
        }

        await api.post('/api/comments/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })

        this.resetForm()
        this.$emit('submitted')
      } catch (error) {
        if (error.response && error.response.data.errors) {
          this.errors = error.response.data.errors
        } else {
          console.error('Error submitting comment:', error)
        }
      } finally {
        this.isSubmitting = false
      }
    },
    resetForm() {
      this.form = {
        username: '',
        email: '',
        homepage: '',
        text: ''
      }
      this.removePreview()
      this.showPreview = false
    }
  }
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
  display: flex;
  align-items: center;
  gap: 5px;
}

.error-message::before {
  content: "⚠️";
  font-size: 0.9rem;
}

.preview-container {
  position: relative;
  display: inline-block;
  margin-top: 15px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
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

.file-upload-container {
  position: relative;
  margin-top: 10px;
}

.file-upload-container input[type="file"] {
  position: absolute;
  left: 0;
  top: 0;
  opacity: 0;
  width: 100%;
  height: 100%;
  cursor: pointer;
}

.file-upload-label {
  display: inline-block;
  padding: 10px 20px;
  background: #f8f9fa;
  border: 2px dashed #d6dbdf;
  border-radius: 8px;
  color: #7f8c8d;
  font-weight: 500;
  transition: all 0.3s ease;
  cursor: pointer;
  text-align: center;
  width: 100%;
}

.file-upload-label:hover {
  background: #ecf0f1;
  border-color: #3498db;
  color: #3498db;
}

.file-upload-label i {
  margin-right: 8px;
  font-size: 1.2rem;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
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
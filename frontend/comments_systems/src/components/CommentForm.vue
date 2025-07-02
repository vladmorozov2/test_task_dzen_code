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
        <div v-if="errors.homepage" class="error-message">{{ errors.homepage }}</div>
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
          :class="{ error: errors.text || htmlErrors.length }"
          rows="5"
        ></textarea>
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
        <input
          type="file"
          ref="fileInput"
          @change="handleFileUpload"
          accept="image/jpeg,image/png,image/gif,.txt"
        />
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
    
    <Lightbox 
      v-if="lightboxVisible" 
      :imageUrl="currentImage" 
      @close="lightboxVisible = false" 
    />
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
      htmlErrors: [],
      attachment: null,
      previewImage: null,
      fileError: '',
      showPreview: false,
      isSubmitting: false,
      lightboxVisible: false,
      currentImage: null
    }
  },
  methods: {
    validateHTML() {
      this.htmlErrors = []
      const text = this.form.text
      
      // 1. Check for allowed tags only
      const allowedTags = ['a', 'code', 'i', 'strong']
      const tagRegex = /<\/?([a-z]+)[^>]*>/gi
      let match
      const foundTags = new Set()

      while ((match = tagRegex.exec(text)) !== null) {
        const tagName = match[1].toLowerCase()
        if (!allowedTags.includes(tagName)) {
          this.htmlErrors.push(`Disallowed HTML tag: <${tagName}>`)
        }
        foundTags.add(tagName)
      }

      // 2. Check for proper tag nesting and closing
      const stack = []
      const fullTagRegex = /<\/?([a-z]+)[^>]*>/gi
      let result
      let lastIndex = 0

      while ((result = fullTagRegex.exec(text)) !== null) {
        const fullTag = result[0]
        const tagName = result[1].toLowerCase()
        
        // Validate attributes for this tag
        const attrErrors = this.validateTagAttributes(fullTag, tagName)
        if (attrErrors.length) {
          this.htmlErrors.push(...attrErrors)
        }

        if (fullTag.startsWith('</')) {
          // Closing tag
          if (stack.length === 0) {
            this.htmlErrors.push(`Unmatched closing tag: </${tagName}>`)
          } else if (stack[stack.length - 1] !== tagName) {
            this.htmlErrors.push(`Tag mismatch: expected </${stack[stack.length - 1]}>, found </${tagName}>`)
          } else {
            stack.pop()
          }
        } else {
          // Opening tag
          stack.push(tagName)
        }
      }


      if (stack.length > 0) {
        stack.forEach(tag => {
          this.htmlErrors.push(`Unclosed tag: <${tag}>`)
        })
      }

      return this.htmlErrors.length === 0
    },

    validateTagAttributes(tag, tagName) {
      const errors = []
      

      if (tagName === 'a') {
      
        const hasHref = /href=["']([^"']*)["']/i.test(tag)
        if (!hasHref) {
          errors.push('<a> tag must have href attribute')
        }

   
        const allowedAttrs = ['href', 'title']
        const attrRegex = /\s([a-z-]+)=["']/gi
        let attrMatch
        
        while ((attrMatch = attrRegex.exec(tag)) !== null) {
          const attrName = attrMatch[1].toLowerCase()
          if (!allowedAttrs.includes(attrName)) {
            errors.push(`Disallowed attribute in <a> tag: ${attrName}`)
          }
        }

   
        const hrefMatch = tag.match(/href=["']([^"']*)["']/i)
        if (hrefMatch && !this.isValidUrl(hrefMatch[1])) {
          errors.push(`Invalid URL in href attribute: ${hrefMatch[1]}`)
        }
      } 
      else if (tag.includes('=')) {
        errors.push(`<${tagName}> tag should not have any attributes`)
      }

      return errors
    },

    isValidUrl(url) {
      if (!url) return false
      
     
      if (url.trim().toLowerCase().startsWith('javascript:')) {
        return false
      }
      
      try {
       
        new URL(url)
        return true
      } catch {
        return false
      }
    },

    handleFileUpload(event) {
      const file = event.target.files[0]
      if (!file) return

      const validImageTypes = ['image/jpeg', 'image/png', 'image/gif']
      const maxImageSize = 100 * 1024

      
      this.previewImage = null
      this.attachment = null
      this.fileError = ''

      if (validImageTypes.includes(file.type)) {
        if (file.size > maxImageSize) {
          this.fileError = 'Image size exceeds 100KB limit'
          return
        }
        
        const img = new Image()
        const reader = new FileReader()
        
        reader.onload = (e) => {
          img.src = e.target.result
          
          img.onload = () => {
            
            const maxWidth = 320
            const maxHeight = 240
            let width = img.width
            let height = img.height
            
            if (width > maxWidth || height > maxHeight) {
              const ratio = Math.min(maxWidth / width, maxHeight / height)
              width = Math.floor(width * ratio)
              height = Math.floor(height * ratio)
              
              const canvas = document.createElement('canvas')
              canvas.width = width
              canvas.height = height
              const ctx = canvas.getContext('2d')
              ctx.drawImage(img, 0, 0, width, height)
              
              this.previewImage = canvas.toDataURL(file.type)
            } else {
              this.previewImage = e.target.result
            }
            
            this.attachment = {
              type: 'image',
              name: file.name,
              size: file.size,
              data: this.previewImage
            }
          }
        }
        
        reader.readAsDataURL(file)
      } else if (file.type === 'text/plain' || file.name.toLowerCase().endsWith('.txt')) {
        if (file.size > 100 * 1024) {
          this.fileError = 'Text file size exceeds 100KB limit'
          return
        }
        
        this.attachment = {
          type: 'text',
          name: file.name,
          size: file.size,
          data: null
        }
      } else {
        this.fileError = 'Invalid file type. Only JPG, PNG, GIF, or TXT allowed'
      }
    },

    removePreview() {
      this.previewImage = null
      this.attachment = null
      this.$refs.fileInput.value = ''
      this.fileError = ''
    },

    openLightbox(imageUrl) {
      this.currentImage = imageUrl
      this.lightboxVisible = true
    },

    formatFileSize(bytes) {
      if (bytes === 0) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2) + ' ' + sizes[i])
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
      this.htmlErrors = []
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
      } else {
        // Validate HTML content
        if (!this.validateHTML()) {
          isValid = false
        }
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

        if (this.attachment) {
          if (this.attachment.type === 'image') {
            // Convert data URL to blob
            const blob = this.dataURLtoBlob(this.attachment.data)
            formData.append('attachment', blob, this.attachment.name)
          } else {
            // For text files, we need to get the file from input
            const fileInput = this.$refs.fileInput
            if (fileInput.files.length > 0) {
              formData.append('attachment', fileInput.files[0])
            }
          }
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
          this.errors.text = 'Error submitting comment. Please try again.'
        }
      } finally {
        this.isSubmitting = false
      }
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

    resetForm() {
      this.form = {
        username: '',
        email: '',
        homepage: '',
        text: ''
      }
      this.removePreview()
      this.showPreview = false
      this.htmlErrors = []
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
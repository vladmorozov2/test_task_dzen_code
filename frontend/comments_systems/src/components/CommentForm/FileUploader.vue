<template>
  <div class="form-group">
    <label>Attachment</label>
    <input
      type="file"
      ref="fileInput"
      @change="handleFileChange"
      accept="image/jpeg,image/png,image/gif,.txt"
    />
    
    <div v-if="previewImage" class="preview-container">
      <img
        :src="previewImage"
        alt="Preview"
        class="preview-image"
        @click="$emit('preview-click', previewImage)"
      />
      <button type="button" @click="removeFile" class="remove-btn">×</button>
    </div>
    
    <div v-if="error" class="error-message">{{ error }}</div>
    
    <div v-if="modelValue && modelValue.type === 'text'" class="attachment-info">
      <div class="file-icon">📄</div>
      <div class="file-name">{{ modelValue.name }}</div>
      <div class="file-size">{{ formatFileSize(modelValue.size) }}</div>
    </div>
  </div>
</template>

<script>
import { ref, watch } from 'vue'
import { validateFile, readFileAsDataURL } from '@/utils/fileUtils'

export default {
  name: 'FileUploader',
  props: {
    modelValue: {
      type: Object,
      default: null
    },
    previewImage: {
      type: String,
      default: null
    },
    error: {
      type: String,
      default: ''
    }
  },
  emits: ['update:modelValue', 'update:previewImage', 'remove', 'preview-click'],
  setup(props, { emit }) {
    const fileInput = ref(null)

    const handleFileChange = async (event) => {
      const file = event.target.files[0]
      if (!file) return

      try {
        const validationError = validateFile(file, {
          allowedTypes: ['image/jpeg', 'image/png', 'image/gif', 'text/plain'],
          maxSize: 5 * 1024 * 1024 // 5MB
        })

        if (validationError) {
          emit('update:modelValue', null)
          emit('update:previewImage', null)
          emit('update:error', validationError)
          return
        }

        const fileData = {
          name: file.name,
          size: file.size,
          type: file.type.startsWith('image/') ? 'image' : 'text',
          file
        }

        emit('update:modelValue', fileData)

        if (fileData.type === 'image') {
          const dataUrl = await readFileAsDataURL(file)
          emit('update:previewImage', dataUrl)
        } else {
          emit('update:previewImage', null)
        }

        emit('update:error', '')
      } catch (err) {
        console.error('File processing error:', err)
        emit('update:error', 'Error processing file')
      }
    }

    const removeFile = () => {
      if (fileInput.value) {
        fileInput.value.value = ''
      }
      emit('update:modelValue', null)
      emit('update:previewImage', null)
      emit('update:error', '')
      emit('remove')
    }

    const formatFileSize = (bytes) => {
      if (bytes < 1024) return `${bytes} bytes`
      if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
      return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
    }

    return {
      fileInput,
      handleFileChange,
      removeFile,
      formatFileSize
    }
  }
}
</script>

<style scoped>
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
  display: flex;
  align-items: center;
  gap: 10px;
}

.file-icon {
  font-size: 24px;
}

.file-name {
  font-weight: bold;
}

.file-size {
  font-size: 0.85rem;
  color: #666;
}

.error-message {
  color: #e74c3c;
  font-size: 0.9rem;
  margin-top: 8px;
  font-weight: 500;
}
</style>
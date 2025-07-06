<template>
  <div class="preview-section">
    <h3>Comment Preview</h3>
    <div class="preview-content">
      <div class="comment-preview" v-html="sanitizedText"></div>
      
      <div v-if="previewImage" class="preview-image-container">
        <img
          :src="previewImage"
          alt="Preview"
          @click="$emit('preview-click', previewImage)"
        />
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
</template>

<script>
import { computed } from 'vue'
import { sanitizeHTML } from '@/utils/htmlSanitizer'

export default {
  name: 'CommentPreview',
  props: {
    text: {
      type: String,
      default: ''
    },
    previewImage: {
      type: String,
      default: null
    },
    attachment: {
      type: Object,
      default: null
    }
  },
  emits: ['preview-click'],
  setup(props) {
    const sanitizedText = computed(() => sanitizeHTML(props.text))

    const formatFileSize = (bytes) => {
      if (bytes < 1024) return `${bytes} bytes`
      if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
      return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
    }

    return {
      sanitizedText,
      formatFileSize
    }
  }
}
</script>

<style scoped>
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

.comment-preview {
  line-height: 1.6;
  margin-bottom: 15px;
}

.preview-image-container {
  margin: 15px 0;
}

.preview-image-container img {
  max-width: 100%;
  max-height: 300px;
  border-radius: 4px;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.preview-image-container img:hover {
  transform: scale(1.02);
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

.file-icon {
  font-size: 24px;
  margin-right: 10px;
}

.file-info {
  display: flex;
  flex-direction: column;
}

.file-name {
  font-weight: bold;
}

.file-size {
  font-size: 0.85rem;
  color: #666;
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
</style>
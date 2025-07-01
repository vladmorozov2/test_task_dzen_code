<template>
  <div :style="indentStyle" class="comment-item">
    <div class="comment-header">
      <span class="username">{{ comment.username }}</span>
      <span class="email">{{ comment.sender }}</span>
      <span class="date">{{ formatDate(comment.created_at) }}</span>
    </div>
    <div class="comment-text">{{ comment.text }}</div>

    <div v-if="comment.attachment" class="attachment-container">
      <div v-if="comment.attachment.type === 'image'">
        <img :src="comment.attachment.data" alt="Attachment" class="attachment-image"
          @click="openLightbox(comment.attachment.data)">
        <div class="attachment-name">{{ comment.attachment.name }}</div>
      </div>
      <div v-else class="text-attachment">
        <a :href="comment.attachment.data || '#'" :download="comment.attachment.name" class="attachment-link">
          <div class="file-icon">📄</div>
          <div class="file-info">
            <div class="file-name">{{ comment.attachment.name }}</div>
            <div class="file-size">{{ formatFileSize(comment.attachment.size) }}</div>
          </div>
        </a>
      </div>
    </div>

    <div class="comment-actions">
      <button @click="toggleReply" class="reply-btn">
        {{ showReply ? 'Cancel' : 'Reply' }}
      </button>
      <button v-if="childComments.length" @click="showChildren = !showChildren" class="toggle-replies-btn">
        {{ showChildren ? 'Hide Replies' : `Show Replies (${childComments.length})` }}
      </button>
    </div>

    <div v-if="showReply" class="reply-form">
      <CommentForm :parentId="comment.id" @submitted="onReplySubmitted" @cancel="toggleReply" />
    </div>

    <div class="child-comments" v-if="childComments.length && showChildren">
      <CommentItem v-for="child in childComments" :key="child.id" :comment="child"
        :child-comments="childCommentsMap[child.id] || []" :child-comments-map="childCommentsMap" :depth="depth + 1" />
    </div>

    <Lightbox v-if="lightboxVisible" :imageUrl="currentImage" @close="lightboxVisible = false" />
  </div>
</template>

<script>
import CommentForm from './CommentForm.vue'
import Lightbox from './Lightbox.vue'

export default {
  name: 'CommentItem',
  components: { CommentForm, Lightbox },
  props: {
    comment: Object,
    childComments: Array,
    childCommentsMap: Object,
    depth: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      showReply: false,
      showChildren: true,
      lightboxVisible: false,
      currentImage: null
    }
  },
  computed: {
    indentStyle() {
      return { marginLeft: `${this.depth * 20}px` }
    }
  },
  methods: {
    toggleReply() {
      this.showReply = !this.showReply
    },
    onReplySubmitted() {
      this.showReply = false
      this.$emit('reply-submitted')
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleString()
    },
    formatFileSize(bytes) {
      if (bytes === 0) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2) + ' ' + sizes[i])
    },
    openLightbox(imageUrl) {
      this.currentImage = imageUrl
      this.lightboxVisible = true
    }
  }
}
</script>

<style scoped>
.comment-item {
  border: 1px solid #eee;
  padding: 15px;
  margin-bottom: 15px;
  background: #fafafa;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.comment-header {
  display: flex;
  gap: 15px;
  margin-bottom: 10px;
  font-size: 0.9em;
  color: #666;
}

.username {
  font-weight: bold;
  color: #333;
}

.attachment-container {
  margin: 10px 0;
  padding: 10px;
  background-color: #fff;
  border: 1px solid #eee;
  border-radius: 4px;
}

.attachment-image {
  max-width: 100%;
  max-height: 240px;
  border-radius: 4px;
  cursor: pointer;
  transition: transform 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.attachment-image:hover {
  transform: scale(1.02);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.attachment-name {
  margin-top: 5px;
  font-size: 0.8em;
  color: #666;
}

.text-attachment {
  display: flex;
  align-items: center;
  padding: 8px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  background: #f8f9fa;
}

.attachment-link {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: inherit;
}

.file-icon {
  font-size: 24px;
}

.file-info {
  display: flex;
  flex-direction: column;
}

.file-name {
  font-weight: bold;
}

.file-size {
  font-size: 0.8em;
  color: #666;
}

.comment-actions {
  margin-top: 15px;
  display: flex;
  gap: 10px;
}

.reply-btn {
  background: transparent;
  border: 1px solid #3b82f6;
  color: #3b82f6;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.reply-btn:hover {
  background-color: #3b82f6;
  color: white;
}

.toggle-replies-btn {
  background: transparent;
  border: 1px solid #10b981;
  color: #10b981;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.toggle-replies-btn:hover {
  background-color: #10b981;
  color: white;
}

.reply-form {
  margin-top: 15px;
  padding: 15px;
  border-left: 3px solid #3b82f6;
  background: #fff;
  border-radius: 0 4px 4px 0;
}
</style>
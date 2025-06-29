<!-- src/components/CommentItem.vue -->
<template>
  <tr class="comment-item" :class="{'reply-comment': depth > 0}">
    <td>{{ comment.username }}</td>
    <td>{{ comment.email }}</td>
    <td>{{ formatDate(comment.created_at) }}</td>
    <td>
      <div v-html="comment.text"></div>
      <button v-if="depth < 3" @click="toggleReply" class="reply-btn">
        {{ showReply ? 'Cancel' : 'Reply' }}
      </button>
      
      <!-- Reply Form -->
      <CommentForm 
        v-if="showReply" 
        class="reply-form"
        @comment-added="handleCommentAdded"
      />
    </td>
    <td>
      <AttachmentPreview :attachment="comment.attachment" />
    </td>
  </tr>
  
  <!-- Child Comments -->
  <template v-if="comment.replies && comment.replies.length > 0">
    <CommentItem 
      v-for="reply in comment.replies" 
      :key="reply.id" 
      :comment="reply"
      :depth="depth + 1"
      @reply="handleReply"
    />
  </template>
</template>

<script>
import CommentForm from './CommentForm.vue'
import AttachmentPreview from './AttachmentPreview.vue'

export default {
  components: { CommentForm, AttachmentPreview },
  props: {
    comment: Object,
    depth: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      showReply: false
    }
  },
  methods: {
    formatDate(dateString) {
      return new Date(dateString).toLocaleString()
    },
    toggleReply() {
      this.showReply = !this.showReply
    },
    handleCommentAdded() {
      this.showReply = false
      this.$emit('comment-added')
    },
    handleReply(comment) {
      this.$emit('reply', comment)
    }
  }
}
</script>

<style scoped>

</style>
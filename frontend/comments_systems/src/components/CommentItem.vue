<template>
  <div :style="indentStyle" class="comment-item">
    <div class="comment-text" v-html="comment.text"></div> <!-- если text с HTML -->
    <div>{{ comment }}</div>
    <div v-if="comment.attachment_url" class="comment-attachment">
      <img :src="comment.attachment_url" alt="Attachment" class="attachment-image" />
    </div>
    
    <div class="comment-id">Comment id: {{ comment.id }}</div>
    <div class="comment-created-at">Created at: {{ formatDate(comment.created_at) }}</div>
    <div class="comment-sender">Sender: {{ comment.sender }}</div>
    <div class="comment-username">Username: {{ comment.username }}</div>

    <button @click="toggleReply" class="reply-btn">
      {{ showReply ? 'Cancel' : 'Reply' }}
    </button>

    <div v-if="showReply" class="reply-form">
      <CommentForm
        :parentId="comment.id"
        @submitted="onReplySubmitted"
        @cancel="toggleReply"
      />
    </div>

    <div class="child-comments" v-if="childComments.length">
      <CommentItem
        v-for="child in childComments"
        :key="child.id"
        :comment="child"
        :child-comments="childCommentsMap[child.id] || []"
        :child-comments-map="childCommentsMap"
        :depth="depth + 1"
        @reply-submitted="handleReplySubmitted"
      />
    </div>
  </div>
</template>

<script>
import CommentForm from './CommentForm.vue'

export default {
  name: 'CommentItem',
  components: { CommentForm },
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
      showReply: false
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
    onReplySubmitted(newComment) {
      this.showReply = false
      this.$emit('reply-submitted', newComment)
    },
    handleReplySubmitted(newComment) {
      this.$emit('reply-submitted', newComment)
    },
    formatDate(dateStr) {
      return new Date(dateStr).toLocaleString()
    }
  }
}
</script>

<style scoped>
.comment-item {
  border: 1px solid #ddd;
  padding: 10px;
  margin-bottom: 10px;
  background: #fafafa;
}

.comment-attachment {
  margin: 10px 0;
}

.attachment-image {
  max-width: 320px; /* ограничение ширины */
  max-height: 240px; /* ограничение высоты */
  border-radius: 8px;
  object-fit: contain;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.reply-btn {
  background: transparent;
  border: none;
  color: #3b82f6;
  cursor: pointer;
  margin-bottom: 8px;
}

.reply-btn:hover {
  text-decoration: underline;
}

.reply-form {
  margin-top: 10px;
  padding-left: 10px;
  border-left: 2px solid #3b82f6;
}
</style>

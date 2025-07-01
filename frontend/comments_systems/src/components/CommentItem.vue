<template>
  <div :style="indentStyle" class="comment-item">
    <div class="comment-header">
      <span class="username">{{ comment.username }}</span>
      <span class="email">{{ comment.sender }}</span>
      <span class="date">{{ formatDate(comment.created_at) }}</span>
    </div>
    <div class="comment-text">{{ comment.text }}</div>

    <div class="comment-actions">
      <button @click="toggleReply" class="reply-btn">
        {{ showReply ? 'Cancel' : 'Reply' }}
      </button>
      <button 
        v-if="childComments.length"
        @click="showChildren = !showChildren"
        class="toggle-replies-btn"
      >
        {{ showChildren ? 'Hide Replies' : `Show Replies (${childComments.length})` }}
      </button>
    </div>

    <div v-if="showReply" class="reply-form">
      <CommentForm
        :parentId="comment.id"
        @submitted="onReplySubmitted"
        @cancel="toggleReply"
      />
    </div>

    <div class="child-comments" v-if="childComments.length && showChildren">
      <CommentItem
        v-for="child in childComments"
        :key="child.id"
        :comment="child"
        :child-comments="childCommentsMap[child.id] || []"
        :child-comments-map="childCommentsMap"
        :depth="depth + 1"
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
      showReply: false,
      showChildren: true
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
    }
  }
}
</script>

<style scoped>
.comment-item {
  border: 1px solid #eee;
  padding: 10px;
  margin-bottom: 10px;
  background: #fafafa;
}

.comment-header {
  display: flex;
  gap: 15px;
  margin-bottom: 5px;
  font-size: 0.9em;
  color: #666;
}

.username {
  font-weight: bold;
}

.comment-actions {
  margin-top: 10px;
  display: flex;
  gap: 8px;
}

.reply-btn {
  background: transparent;
  border: 1px solid #3b82f6;
  color: #3b82f6;
  padding: 3px 8px;
  border-radius: 4px;
  cursor: pointer;
}

.reply-btn:hover {
  background-color: #3b82f6;
  color: white;
}

.toggle-replies-btn {
  background: transparent;
  border: 1px solid #10b981;
  color: #10b981;
  padding: 3px 8px;
  border-radius: 4px;
  cursor: pointer;
}

.toggle-replies-btn:hover {
  background-color: #10b981;
  color: white;
}

.reply-form {
  margin-top: 10px;
  padding: 10px;
  border-left: 3px solid #3b82f6;
  background: #fff;
}
</style>
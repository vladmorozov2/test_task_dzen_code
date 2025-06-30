<template>
  <div :style="indentStyle" class="comment-item">
    <div class="comment-text">Comment text:{{ comment.text }}</div>
    <div class="comment-id">Comment id: {{ comment.id }}</div>
    <div class="comment-created-at">Created at: {{ comment.created_at }}</div>
    <div class="comment-sender">Sender: {{ comment.sender }}</div>

    <button @click="toggleReply" class="reply-btn">
      {{ showReply ? 'Cancel' : 'Reply' }}
    </button>

    <!-- Форма відповіді -->
    <div v-if="showReply" class="reply-form">
      <CommentForm
        :parentId="comment.id"
        @submitted="onReplySubmitted"
        @cancel="toggleReply"
      />
    </div>

    <!-- Відображення дочірніх коментарів рекурсивно -->
    <div class="child-comments" v-if="childComments.length">
      <CommentItem
        v-for="child in childComments"
        :key="child.id"
        :comment="child"
        :child-comments="childCommentsMap[child.id] || []"
        :child-comments-map="childCommentsMap"
        :depth="depth + 1"
        @reply-submitted="$emit('reply-submitted')"
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
      // Закриваємо форму
      this.showReply = false
      // Повідомляємо батька, щоб обновити список
      this.$emit('reply-submitted', newComment)
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

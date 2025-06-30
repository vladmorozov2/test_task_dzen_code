<template>
  <div :style="indentStyle" class="comment-item">
    <div class="text">{{ comment.text }}</div>

    <!-- Render children recursively -->
    <div class="child-comments" v-if="childComments.length">
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
export default {
  name: 'CommentItem',
  props: {
    comment: Object,
    childComments: Array,
    childCommentsMap: Object,
    depth: {
      type: Number,
      default: 0
    }
  },
  computed: {
    indentStyle() {
      return {
        marginLeft: `${this.depth * 20}px`
      }
    }
  }
}
</script>

<style scoped>
.comment-item {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 8px;
  background: #f9f9f9;
}

.child-comments {
  margin-top: 8px;
}
</style>

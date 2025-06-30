<template>
  <div class="comment-list">
    <CommentItem
      v-for="comment in rootComments"
      :key="comment.id"
      :comment="comment"
      :child-comments="childCommentsMap[comment.id] || []"
      :child-comments-map="childCommentsMap"
      :depth="0"
    />
  </div>
</template>

<script>
import CommentItem from './CommentItem.vue'

export default {
  name: 'CommentList',
  components: { CommentItem },
  props: {
    comments: Array
  },
  computed: {
    rootComments() {
      return this.comments.filter(c => c.parent_comment === null)
    },
    childCommentsMap() {
      const map = {}
      this.comments.forEach(comment => {
        if (comment.parent_comment !== null) {
          if (!map[comment.parent_comment]) {
            map[comment.parent_comment] = []
          }
          map[comment.parent_comment].push(comment)
        }
      })
      return map
    }
  }
}
</script>

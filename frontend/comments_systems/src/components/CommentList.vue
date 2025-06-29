<!-- src/components/CommentList.vue -->
<template>
  <div class="comment-list">
    <h2>Comments</h2>
    
    <!-- Sorting Controls -->
    
    <!-- Comments Table -->
    <table class="comments-table">
      <thead>
        <tr>
          <th>User</th>
          <th>Email</th>
          <th>Date</th>
          <th>Comment</th>
          <th>Attachment</th>
        </tr>
      </thead>
      <tbody>
        <div v-for="comment in comments" :key="comment.id">
          {{ comment}}

        </div>
      </tbody>
    </table>
    
    <!-- Pagination -->
    
  </div>
</template>

<script>
import CommentItem from './CommentItem.vue'

export default {
  components: { CommentItem },
  props: {
    comments: Array,
    pagination: Object
  },
  data() {
    return {
      sortField: 'created_at',
      sortDirection: 'desc',
      currentPage: 1
    }
  },
  computed: {
    totalPages() {
      return this.pagination.totalPages || 1
    }
  },
  watch: {
    pagination: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.currentPage = newVal.currentPage
        }
      }
    }
  },
  methods: {
    emitSortChange() {
      this.$emit('sort-changed', {
        field: this.sortField,
        direction: this.sortDirection
      })
    },
    changePage(page) {
      if (page !== this.currentPage) {
        this.currentPage = page
        this.$emit('page-changed', page)
      }
    },
    handleReply(comment) {
      // Scroll to form and prefill reply
      this.$emit('reply-to-comment', comment)
    }
  }
}
</script>

<style scoped>
</style>
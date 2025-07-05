<!-- src/pages/CommentsPage.vue -->
<template>
  <div>
    <CommentForm @comment-added="fetchComments" ref="commentForm" />
    <CommentList 
      ref="commentList"
      :comments="comments"
      :pagination="pagination"
      @sort-changed="handleSortChange"
      @page-changed="handlePageChange"
    />
  </div>
</template>

<script>
import CommentForm from '@/components/CommentForm.vue'
import CommentList from '@/components/CommentList.vue'
import api from '@/axios'

export default {
  components: { CommentForm, CommentList },
  data() {
    return {
      comments: [],
      pagination: {
        currentPage: 1,
        totalPages: 1,
        perPage: 25
      },
      sort: {
        field: 'created_at',
        direction: 'desc'
      }
    }
  },
  mounted() {
    this.fetchComments()
  },
  methods: {
    async fetchComments() {
      try {
        const params = {
          page: this.pagination.currentPage,
          per_page: this.pagination.perPage,
          sort_by: this.sort.field,
          sort_dir: this.sort.direction
        }

        const response = await api.get('/api/comments/', { params })

        this.comments = response.data.data
        this.pagination.totalPages = response.data.meta.last_page
      } catch (error) {
        console.error('Error fetching comments:', error)
      }
    },
    handleReplyToComment(comment) {
      this.$refs.commentForm.$el.scrollIntoView({ behavior: 'smooth' });
      this.$refs.commentForm.setParentComment(comment.id);
      this.$refs.commentForm.prefillText(`>>${comment.id} `);
    },
    handleSortChange(sortConfig) {
      this.sort = sortConfig
      this.fetchComments()
    },
    handlePageChange(page) {
      this.pagination.currentPage = page
      this.fetchComments()
    }
  }
}
</script>

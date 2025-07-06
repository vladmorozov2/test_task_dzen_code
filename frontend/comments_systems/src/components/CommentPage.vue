<!-- src/pages/CommentsPage.vue -->
<template>
  <div>
    <CommentForm @comment-added="fetchComments" ref="commentForm" />
    <CommentList ref="commentList" :comments="comments" :pagination="pagination" @sort-changed="handleSortChange"
      @page-changed="handlePageChange" />
    <div class="pagination-controls">
      <button :disabled="pagination.currentPage >= pagination.totalPages" @click="loadNextPage">
        Load more
      </button>
    </div>

  </div>
</template>

<script>
import CommentForm from '@/components/CommentForm.vue'
import CommentList from '@/components/CommentList.vue'
import api from '../axios'

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
    async fetchComments(append = false) {
      try {
        const params = {
          page: this.pagination.currentPage,
          per_page: this.pagination.perPage,
          sort_by: this.sort.field,
          sort_dir: this.sort.direction,
        }
        const response = await api.get('/api/comments/', { params })

        if (append) {
          this.comments = [...this.comments, ...response.data.data]
        } else {
          this.comments = response.data.data
        }

        this.pagination.totalPages = response.data.meta.last_page
        this.pagination.currentPage = response.data.meta.current_page
        this.pagination.perPage = response.data.meta.per_page
      } catch (error) {
        console.error('Error fetching comments:', error)
      }
    },
    async loadNextPage() {
      if (this.pagination.currentPage >= this.pagination.totalPages) return

      this.pagination.currentPage += 1
      await this.fetchComments(true)
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


<style scoped>
.pagination-controls {
  text-align: center;
  margin: 20px 0;
}

.pagination-controls button {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 10px 24px;
  font-size: 1rem;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.pagination-controls button:hover:not(:disabled) {
  background-color: #2980b9;
}

.pagination-controls button:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
}
</style>
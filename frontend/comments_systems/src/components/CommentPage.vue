<template>
  <div>
    <CommentForm @comment-added="loadComments" ref="commentForm" />
    <CommentList ref="commentList" :comments="comments" :pagination="pagination" @sort-changed="handleSortChange"
      @page-changed="handlePageChange" />
    <div v-if="pagination.currentPage < pagination.totalPages" class="pagination-controls">
      <button @click="loadNextPage">Load more</button>
    </div>
  </div>
</template>

<script>
import CommentForm from '@/components/CommentForm/CommentForm.vue'
import CommentList from '@/components/CommentList.vue'
import { fetchComments } from '@/services/commentService'

export default {
  components: { CommentForm, CommentList },
  data() {
    return {
      comments: [],
      pagination: {
        currentPage: 1,
        totalPages: 1,
        perPage: 25,
      },
      sort: {
        field: 'created_at',
        direction: 'desc',
      },
    }
  },
  mounted() {
    this.loadComments()
  },
  methods: {
    async loadComments(append = false) {
      try {
        const data = await fetchComments({
          page: this.pagination.currentPage,
          perPage: this.pagination.perPage,
          sort: this.sort,
        })

        this.comments = append
          ? [...this.comments, ...data.data]
          : data.data

        Object.assign(this.pagination, {
          currentPage: data.meta.current_page,
          totalPages: data.meta.last_page,
          perPage: data.meta.per_page,
        })
      } catch (error) {
        console.error('Error fetching comments:', error)
      }
    },

    async loadNextPage() {
      if (this.pagination.currentPage >= this.pagination.totalPages) return
      this.pagination.currentPage += 1
      await this.loadComments(true)
    },

    handleSortChange(sortConfig) {
      this.sort = sortConfig
      this.pagination.currentPage = 1
      this.loadComments()
    },

    handlePageChange(page) {
      this.pagination.currentPage = page
      this.loadComments()
    },
  },
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

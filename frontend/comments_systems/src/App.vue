<!-- src/App.vue -->
<template>
  <div class="app-container">
    <div v-for="comment in comments" :key="comment.id">
      <div>

        Id message: {{ comment.message }}
        <br>
        ID sender {{ comment.sender }}
        <br>
        Message text: {{ comment.text }}
        <br>
        Created at: {{ comment.created_at }}
      </div>

    </div>
  </div>
</template>

<script>
import CommentForm from './components/CommentForm.vue'
import CommentList from './components/CommentList.vue'
import api from './axios' // ⚠️ ІМПОРТ кастомного інстансу axios

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
        this.comments = response.data
        console.log('Comments fetched:', this.comments)
        console.log('Comments fetched:', response.data)
        
      } catch (error) {
        console.error('Error fetching comments:', error)
      }
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
.app-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}
</style>
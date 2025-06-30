<!-- src/App.vue -->
<template>
  <div class="app-container">
    <CommentForm @comment-added="fetchComments" />
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
import CommentForm from './components/CommentForm.vue'
import CommentList from './components/CommentList.vue'
import api from './axios'  

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
      // 1. Прокрутка к форме
      this.$refs.commentForm.$el.scrollIntoView({ behavior: 'smooth' });
      
      // 2. Установка parent_id для ответа
      this.$refs.commentForm.setParentComment(comment.id);
      
      // 3. Опционально: префилл текста
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
.app-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #333;
  background-color: #f8f9fa;
  min-height: 100vh;
}

.header {
  text-align: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eaeaea;
}

.header h1 {
  color: #2c3e50;
  font-size: 2.5rem;
  margin-bottom: 10px;
}

.subtitle {
  color: #7f8c8d;
  font-size: 1.1rem;
  margin: 0;
}

@media (max-width: 768px) {
  .app-container {
    padding: 15px;
  }
  
  .header h1 {
    font-size: 2rem;
  }
}

@media (max-width: 480px) {
  .header h1 {
    font-size: 1.7rem;
  }
}
</style>

<style>
/* Глобальные стили */
body {
  margin: 0;
  background-color: #f0f2f5;
  line-height: 1.6;
}

* {
  box-sizing: border-box;
}

a {
  color: #3498db;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

code {
  background-color: #f1f1f1;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  border: 1px solid #ddd;
  font-size: 0.9em;
}

i {
  font-style: italic;
}

strong {
  font-weight: bold;
}

button {
  cursor: pointer;
  transition: all 0.3s ease;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Анимации */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}
</style>

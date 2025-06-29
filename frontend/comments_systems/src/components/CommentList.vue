<!-- src/components/CommentList.vue -->
<template>
  <div class="comment-list">
    <h2>Comments</h2>
    
    <!-- Sorting Controls -->
    <div class="sort-controls">
      <label>Sort by:</label>
      <select v-model="sortField" @change="emitSortChange">
        <option value="username">Username</option>
        <option value="email">Email</option>
        <option value="created_at">Date</option>
      </select>
      
      <label>Direction:</label>
      <select v-model="sortDirection" @change="emitSortChange">
        <option value="asc">Ascending</option>
        <option value="desc">Descending</option>
      </select>
    </div>
    
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
        <CommentItem 
          v-for="comment in comments" 
          :key="comment.id" 
          :comment="comment" 
          @reply="handleReply"
        />
      </tbody>
    </table>
    
    <!-- Pagination -->
    <div class="pagination">
      <button 
        v-for="page in totalPages" 
        :key="page"
        @click="changePage(page)"
        :class="{ active: currentPage === page }"
      >
        {{ page }}
      </button>
    </div>
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
      this.$emit('reply-to-comment', comment)
    }
  }
}
</script>

<style scoped>
.comment-list {
  background-color: #ffffff;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.08);
  border: 1px solid #eef2f6;
  margin-top: 24px;
  transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
}

.comment-list:hover {
  box-shadow: 0 15px 50px rgba(0, 0, 0, 0.12);
  transform: translateY(-3px);
}

.comment-list h2 {
  color: #1a1f36;
  margin-bottom: 28px;
  padding-bottom: 18px;
  border-bottom: 1px solid #edf1f5;
  font-size: 2rem;
  font-weight: 700;
  letter-spacing: -0.5px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.comment-list h2::before {
  content: "💬";
  font-size: 1.8rem;
}

.sort-controls {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 28px;
  padding: 18px;
  background-color: #f8fafc;
  border-radius: 12px;
  flex-wrap: wrap;
  border: 1px solid #e7ebf0;
}

.sort-controls label {
  font-weight: 600;
  color: #2d3748;
  white-space: nowrap;
  font-size: 1.05rem;
}

.sort-controls select {
  padding: 12px 20px;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  background: white;
  font-size: 1.05rem;
  transition: all 0.3s ease;
  cursor: pointer;
  min-width: 140px;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 16px center;
  background-size: 16px;
  appearance: none;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.03);
}

.sort-controls select:focus {
  outline: none;
  border-color: #4299e1;
  box-shadow: 0 0 0 4px rgba(66, 153, 225, 0.2);
}

.comments-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  margin-bottom: 28px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
}

.comments-table th {
  background-color: #2b6cb0;
  color: white;
  text-align: left;
  padding: 20px 24px;
  font-weight: 600;
  font-size: 1.1rem;
  position: sticky;
  top: 0;
  z-index: 10;
}

.comments-table th:first-child {
  border-top-left-radius: 12px;
}

.comments-table th:last-child {
  border-top-right-radius: 12px;
}

.comments-table td {
  padding: 24px;
  border-bottom: 1px solid #f1f5f9;
  vertical-align: top;
  background-color: #ffffff;
  transition: all 0.3s ease;
  position: relative;
}

.comments-table td::before {
  content: "";
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  width: 4px;
  background: transparent;
  transition: background-color 0.3s ease;
}

.comments-table tr:hover td::before {
  background-color: #4299e1;
}

.comments-table tr:last-child td {
  border-bottom: none;
}

.comments-table tr:hover td {
  background-color: #f8fafc;
}

.pagination {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 32px;
  flex-wrap: wrap;
}

.pagination button {
  padding: 12px 20px;
  background: #edf2f7;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-weight: 600;
  color: #2d3748;
  min-width: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.04);
  font-size: 1.05rem;
}

.pagination button:hover:not(.active) {
  background: #e2e8f0;
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
}

.pagination button.active {
  background: #4299e1;
  color: white;
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(66, 153, 225, 0.4);
}

@media (max-width: 992px) {
  .comment-list {
    padding: 24px;
  }
  
  .comments-table {
    display: block;
    overflow-x: auto;
    border-radius: 10px;
  }
  
  .comments-table th,
  .comments-table td {
    padding: 16px 20px;
  }
}

@media (max-width: 768px) {
  .sort-controls {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
    padding: 16px;
  }
  
  .sort-controls > div {
    display: flex;
    flex-direction: column;
    width: 100%;
    gap: 8px;
  }
  
  .sort-controls select {
    width: 100%;
    min-width: auto;
  }
  
  .comments-table th {
    font-size: 1rem;
    padding: 14px 16px;
  }
  
  .comments-table td {
    padding: 18px 16px;
    font-size: 0.95rem;
  }
  
  .pagination button {
    padding: 10px 16px;
    font-size: 0.95rem;
    min-width: 38px;
  }
}

@media (max-width: 480px) {
  .comment-list {
    padding: 20px 16px;
    border-radius: 12px;
  }
  
  .comment-list h2 {
    font-size: 1.7rem;
    padding-bottom: 14px;
  }
  
  .pagination {
    gap: 6px;
  }
  
  .pagination button {
    padding: 8px 14px;
    min-width: 36px;
    font-size: 0.9rem;
  }
}


@keyframes fadeIn {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}

.comment-enter-active {
  animation: fadeIn 0.6s ease;
}

/* Заголовки столбцов */
.comments-table th:nth-child(1) { width: 15%; }
.comments-table th:nth-child(2) { width: 20%; }
.comments-table th:nth-child(3) { width: 15%; }
.comments-table th:nth-child(4) { width: 40%; }
.comments-table th:nth-child(5) { width: 10%; }
</style>
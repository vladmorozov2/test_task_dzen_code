<template>
  <div class="comment-list">
    <table class="comments-table">
      <thead>
        <tr>
          <th @click="setSort('username')">
            User Name 
            <SortIndicator field="username" :current-field="sortField" :direction="sortDirection"/>
          </th>
          <th @click="setSort('sender')">
            E-mail 
            <SortIndicator field="sender" :current-field="sortField" :direction="sortDirection"/>
          </th>
          <th @click="setSort('created_at')">
            Date Added 
            <SortIndicator field="created_at" :current-field="sortField" :direction="sortDirection"/>
          </th>
          <th>Comment</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <template v-for="comment in sortedRootComments" :key="comment.id">
          <tr class="root-comment">
            <td>{{ comment.username }}</td>
            <td>{{ comment.sender }}</td>
            <td>{{ formatDate(comment.created_at) }}</td>
            <td>{{ comment.text }}</td>
            <td>
              <button @click="toggleReply(comment.id)" class="reply-btn">
                {{ replyingTo === comment.id ? 'Cancel' : 'Reply' }}
              </button>
              <button 
                v-if="childCommentsMap[comment.id]?.length"
                @click="toggleReplies(comment.id)"
                class="toggle-replies-btn"
              >
                {{ showReplies[comment.id] ? 'Hide Replies' : `Show Replies (${childCommentsMap[comment.id].length})` }}
              </button>
            </td>
          </tr>
          <tr v-if="replyingTo === comment.id">
            <td colspan="5">
              <CommentForm 
                :parentId="comment.id" 
                @submitted="handleReplySubmitted"
                @cancel="replyingTo = null"
              />
            </td>
          </tr>
          <tr v-if="showReplies[comment.id] && childCommentsMap[comment.id]?.length">
            <td colspan="5">
              <div class="child-comments">
                <CommentItem
                  v-for="child in childCommentsMap[comment.id]"
                  :key="child.id"
                  :comment="child"
                  :child-comments="childCommentsMap[child.id] || []"
                  :child-comments-map="childCommentsMap"
                />
              </div>
            </td>
          </tr>
        </template>
      </tbody>
    </table>
  </div>
</template>

<script>
import CommentItem from './CommentItem.vue'
import CommentForm from './CommentForm.vue'
import SortIndicator from './SortIndicator.vue'

export default {
  name: 'CommentList',
  components: { CommentItem, CommentForm, SortIndicator },
  props: {
    comments: Array
  },
  data() {
    return {
      ws: null,
      localComments: [],
      sortField: 'created_at',
      sortDirection: 'desc',
      replyingTo: null,
      showReplies: {}
    }
  },
  computed: {
    rootComments() {
      return this.localComments.filter(c => c.parent_comment === null)
    },
    childCommentsMap() {
      const map = {}
      this.localComments.forEach(comment => {
        if (comment.parent_comment !== null) {
          if (!map[comment.parent_comment]) {
            map[comment.parent_comment] = []
          }
          map[comment.parent_comment].push(comment)
        }
      })
      return map
    },
    sortedRootComments() {
      return [...this.rootComments].sort((a, b) => {
        let valA = a[this.sortField]
        let valB = b[this.sortField]
        
        if (this.sortField === 'created_at') {
          valA = new Date(valA)
          valB = new Date(valB)
        }
        
        if (typeof valA === 'string') {
          valA = valA.toLowerCase()
          valB = valB.toLowerCase()
        }
        
        if (valA < valB) return this.sortDirection === 'asc' ? -1 : 1
        if (valA > valB) return this.sortDirection === 'asc' ? 1 : -1
        return 0
      })
    }
  },
  methods: {
    setSort(field) {
      if (this.sortField === field) {
        this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc'
      } else {
        this.sortField = field
        this.sortDirection = 'asc'
      }
    },
    toggleReply(commentId) {
      this.replyingTo = this.replyingTo === commentId ? null : commentId
    },
    toggleReplies(commentId) {
      // FIXED: Use direct assignment instead of this.$set
      this.showReplies = {
        ...this.showReplies,
        [commentId]: !this.showReplies[commentId]
      }
    },
    handleReplySubmitted() {
      this.replyingTo = null
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleString()
    },
    connectWebSocket() {
      this.ws = new WebSocket('ws://localhost:8000/ws/comments/')

      this.ws.onopen = () => {
        console.log('WebSocket connected')
      }

      this.ws.onmessage = (event) => {
        const data = JSON.parse(event.data)
        if (data.type === 'new_comment') {
          console.log('New comment received:', data.comment)
          this.localComments.push(data.comment)
        }
      }

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error)
      }

      this.ws.onclose = () => {
        console.warn('WebSocket closed')
      }
    }
  },
  mounted() {
    this.connectWebSocket()
  },
  beforeUnmount() {
    if (this.ws) {
      this.ws.close()
    }
  },
  watch: {
    comments: {
      handler(newComments) {
        this.localComments = [...newComments]
      },
      immediate: true
    }
  }
}
</script>

<style scoped>
.comments-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

.comments-table th, .comments-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.comments-table th {
  background-color: #f2f2f2;
  cursor: pointer;
  position: relative;
}

.root-comment {
  background-color: #f9f9f9;
}

.child-comments {
  padding-left: 30px;
}

.reply-btn {
  background: transparent;
  border: 1px solid #3b82f6;
  color: #3b82f6;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
}

.reply-btn:hover {
  background-color: #3b82f6;
  color: white;
}

.toggle-replies-btn {
  background: transparent;
  border: 1px solid #10b981;
  color: #10b981;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  margin-left: 8px;
}

.toggle-replies-btn:hover {
  background-color: #10b981;
  color: white;
}
</style>
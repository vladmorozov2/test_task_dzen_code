<template>
  <div class="comment-list">
    <table>
      <thead>
        <tr>
          <th @click="changeSort('username')">
            User Name
            <span v-if="sortField === 'username'">{{ sortAsc ? '▲' : '▼' }}</span>
          </th>
          <th @click="changeSort('email')">
            E-mail
            <span v-if="sortField === 'email'">{{ sortAsc ? '▲' : '▼' }}</span>
          </th>
          <th @click="changeSort('created_at')">
            Date Added
            <span v-if="sortField === 'created_at'">{{ sortAsc ? '▲' : '▼' }}</span>
          </th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="comment in sortedRootComments" :key="comment.id">
          <td>{{ comment.username }}</td>
          <td>{{ comment.email }}</td>
          <td>{{ formatDate(comment.created_at) }}</td>
          <td>
            <button @click="toggleReplies(comment.id)">
              {{ openedComments.has(comment.id) ? 'Hide Replies' : 'Show Replies' }}
            </button>
          </td>
        </tr>
        <tr v-for="commentId of openedCommentsArray" :key="'replies-' + commentId">
          <td colspan="4" class="replies-container">
            <div v-if="childCommentsMap[commentId]?.length">
              <CommentItem
                v-for="child in childCommentsMap[commentId]"
                :key="child.id"
                :comment="child"
                :child-comments="childCommentsMap[child.id] || []"
                :child-comments-map="childCommentsMap"
                :depth="1"
                @reply-submitted="onReplySubmitted"
              />
            </div>
            <div v-else>
              No replies.
            </div>
          </td>
        </tr>
      </tbody>
    </table>
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
  data() {
    return {
      localComments: [],
      sortField: 'created_at',
      sortAsc: false,
      openedComments: new Set() // Відкриті root-коментарі з показом відповідей
    }
  },
  computed: {
    rootComments() {
      return this.localComments.filter(c => c.parent_comment === null)
    },
    sortedRootComments() {
      return [...this.rootComments].sort((a, b) => {
        let valA = a[this.sortField]
        let valB = b[this.sortField]

        if (this.sortField === 'created_at') {
          valA = new Date(valA).getTime()
          valB = new Date(valB).getTime()
        } else {
          valA = valA?.toString().toLowerCase() || ''
          valB = valB?.toString().toLowerCase() || ''
        }

        if (valA < valB) return this.sortAsc ? -1 : 1
        if (valA > valB) return this.sortAsc ? 1 : -1
        return 0
      })
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
    openedCommentsArray() {
      return Array.from(this.openedComments)
    }
  },
  methods: {
    changeSort(field) {
      if (this.sortField === field) {
        this.sortAsc = !this.sortAsc
      } else {
        this.sortField = field
        this.sortAsc = true
      }
    },
    formatDate(dateStr) {
      return new Date(dateStr).toLocaleString()
    },
    toggleReplies(commentId) {
      if (this.openedComments.has(commentId)) {
        this.openedComments.delete(commentId)
      } else {
        this.openedComments.add(commentId)
      }
    },
    onReplySubmitted(newComment) {
      this.localComments.push(newComment)
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
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

th, td {
  padding: 0.5rem;
  border: 1px solid #ccc;
  vertical-align: top;
}

th {
  cursor: pointer;
  user-select: none;
}

th span {
  margin-left: 5px;
  font-size: 0.8rem;
  color: #555;
}

.replies-container {
  background-color: #f9f9f9;
  padding-left: 20px;
}
</style>

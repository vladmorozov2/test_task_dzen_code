<template>
  <div class="comment-list">
    <table class="comments-table">
      <thead>
        <tr>
          <th @click="setSort('username')">
            User Name
            <SortIndicator field="username" :current-field="sortField" :direction="sortDirection" />
          </th>
          <th @click="setSort('sender')">
            E-mail
            <SortIndicator field="sender" :current-field="sortField" :direction="sortDirection" />
          </th>
          <th @click="setSort('created_at')">
            Date Added
            <SortIndicator field="created_at" :current-field="sortField" :direction="sortDirection" />
          </th>
          <th>Comment</th>
          <th>Attachments</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <template v-for="comment in sortedRootComments" :key="comment.id">
          <tr class="root-comment">
            <td>{{ comment.username }}</td>
            <td>{{ comment.email }}</td>
            <td>{{ formatDate(comment.created_at) }}</td>
            <td v-html="comment.text"></td>
            <td>
              <div v-if="comment.attachment" class="attachment-cell">
                <div v-if="isImageAttachment(comment.attachment)" class="image-attachment">
                  <img :src="getFullAttachmentUrl(comment.attachment)" alt="Attachment" class="attachment-thumb"
                    @click="openLightbox(getFullAttachmentUrl(comment.attachment))">
                </div>
                <div v-else class="text-attachment">
                  <a :href="getFullAttachmentUrl(comment.attachment)" target="_blank" download>
                    <div class="file-icon">📄</div>
                    <div class="file-name">{{ getFileName(comment.attachment) }}</div>
                  </a>
                </div>
              </div>
            </td>
            <td>
              <button @click="toggleReply(comment.id)" class="reply-btn">
                {{ replyingTo === comment.id ? 'Cancel' : 'Reply' }}
              </button>
              <button v-if="childCommentsMap[comment.id]?.length" @click="toggleReplies(comment.id)"
                class="toggle-replies-btn">
                {{ showReplies[comment.id] ? 'Hide Replies' : `Show Replies (${childCommentsMap[comment.id].length})` }}
              </button>
            </td>
          </tr>
          <tr v-if="replyingTo === comment.id">
            <td colspan="6">
              <CommentForm :parentId="comment.id" @submitted="handleReplySubmitted" @cancel="replyingTo = null" />
            </td>
          </tr>
          <tr v-if="showReplies[comment.id] && childCommentsMap[comment.id]?.length">
            <td colspan="6">
              <div class="child-comments">
                <CommentItem v-for="child in childCommentsMap[comment.id]" :key="child.id" :comment="child"
                  :child-comments="childCommentsMap[child.id] || []" :child-comments-map="childCommentsMap" />
              </div>
            </td>
          </tr>
        </template>
      </tbody>
    </table>

    <Lightbox v-if="lightboxVisible" :imageUrl="currentImage" @close="lightboxVisible = false" />
  </div>
</template>

<script>
import CommentItem from './CommentItem.vue'
import CommentForm from './CommentForm.vue'
import SortIndicator from './SortIndicator.vue'
import Lightbox from './Lightbox.vue'

export default {
  name: 'CommentList',
  components: { CommentItem, CommentForm, SortIndicator, Lightbox },
  props: {
    comments: Array
  },
  data() {
    return {
      ws: null,
      wsConnected: false,
      localComments: [],
      sortField: 'created_at',
      sortDirection: 'desc',
      replyingTo: null,
      showReplies: {},
      lightboxVisible: false,
      currentImage: null,
      apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
      wsBaseUrl: import.meta.env.VITE_WS_BASE_URL || 'ws://localhost:8000'
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
          valA = new Date(valA).getTime()
          valB = new Date(valB).getTime()
        } else if (typeof valA === 'string') {
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
    // Attachment handling methods
    isImageAttachment(attachmentPath) {
      if (!attachmentPath) return false
      const imageExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
      return imageExtensions.some(ext => attachmentPath.toLowerCase().endsWith(ext))
    },
    getFullAttachmentUrl(attachmentPath) {
      if (!attachmentPath) return ''
      // Handle both full URLs and relative paths
      if (attachmentPath.startsWith('http')) {
        return attachmentPath
      }
      // Use API base URL for attachments
      return `${this.apiBaseUrl}${attachmentPath}`
    },
    getFileName(attachmentPath) {
      if (!attachmentPath) return ''
      return attachmentPath.split('/').pop()
    },

    // Comment methods
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
    openLightbox(imageUrl) {
      this.currentImage = imageUrl
      this.lightboxVisible = true
    },
    connectWebSocket() {
      const wsUrl = this.wsBaseUrl;
      console.log('Connecting to WebSocket at:', wsUrl)
      
      // Close existing connection if any
      if (this.ws) {
        this.ws.close();
      }
      
      this.ws = new WebSocket(`${wsUrl}/ws/comments/`);
      console.log('WebSocket instance created:', this.ws);
      this.ws.onopen = () => {
        console.log('WebSocket connected')
        this.wsConnected = true;
      };

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          if (data.type === 'new_comment') {
            console.log('New comment received:', data.comment);
            // Add to beginning of list
            this.localComments = [data.comment, ...this.localComments];
          }
        } catch (e) {
          console.error('Error parsing WebSocket message:', e);
        }
      };

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        this.wsConnected = false;
      };

      this.ws.onclose = () => {
        console.log('WebSocket closed');
        this.wsConnected = false;
        // Attempt reconnect after 3 seconds
        setTimeout(() => this.connectWebSocket(), 3000);
      };
    }
  },
  mounted() {
    this.connectWebSocket();
  },
  beforeUnmount() {
    if (this.ws) {
      this.ws.close();
    }
  },
  watch: {
    comments: {
      handler(newComments) {
        this.localComments = [...newComments];
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

.comments-table th,
.comments-table td {
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

.attachment-cell {
  max-width: 100px;
}

.attachment-thumb {
  max-width: 60px;
  max-height: 40px;
  border-radius: 4px;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.attachment-thumb:hover {
  transform: scale(1.1);
}

.text-attachment {
  display: flex;
  align-items: center;
  gap: 5px;
}

.file-icon {
  font-size: 16px;
}

.file-name {
  font-size: 0.8rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
<template>
  <div class="comment-list">
    <CommentItem
      v-for="comment in rootComments"
      :key="comment.id"
      :comment="comment"
      :child-comments="childCommentsMap[comment.id] || []"
      :child-comments-map="childCommentsMap"
      :depth="0"
    />
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
      ws: null,
      localComments: []  
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
    }
  },
  methods: {
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

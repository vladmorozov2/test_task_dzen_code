<template>
  <div class="app-container">
    <router-view />
  </div>
</template>

<script>
import { onMounted } from 'vue'
import { useAuthStore } from './store/auth'

export default {
  name: 'App',
  setup() {
    const auth = useAuthStore()

    onMounted(() => {
      if (auth.isAuthenticated) {
        auth.fetchUser()
      }
    })
  },
}
</script>

<style scoped>
.app-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f7f7f7;
  min-height: 100vh;
}
</style>

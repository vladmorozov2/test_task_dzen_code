import axios from 'axios'
import { useAuthStore } from './store/auth'  // коригуй шлях під свій

const instance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
})


instance.interceptors.request.use((config) => {
  const authStore = useAuthStore()
  const token = authStore.token
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  console.log('Token in axios interceptor:', token)
  return config
}, (error) => {
  return Promise.reject(error)
})

export default instance

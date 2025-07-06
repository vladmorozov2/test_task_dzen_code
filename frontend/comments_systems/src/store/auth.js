// src/store/auth.js
import { defineStore } from 'pinia'
import axios from '../axios'  

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    user: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
  },

  actions: {
    async login(credentials) {
      try {
        const response = await axios.post('/api/login/', credentials)
        this.token = response.data.access
        localStorage.setItem('token', this.token)

    
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`

        await this.fetchUser()
      } catch (error) {
        throw error
      }
    },

    async register(data) {
      try {
        await axios.post('/api/user/', data)
      } catch (error) {
        throw error
      }
    },

    async fetchUser() {
      if (!this.token) return
      try {
        
        const response = await axios.get('/api/user/')
        this.user = response.data
      } catch (error) {
        this.logout()
      }
    },

    logout() {
      this.token = ''
      this.user = null
      localStorage.removeItem('token')
      delete axios.defaults.headers.common['Authorization']
    },
  },
})

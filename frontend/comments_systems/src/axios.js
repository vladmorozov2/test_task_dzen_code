// src/axios.js
import axios from 'axios'

const instance = axios.create({
  
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',     
})
console.log('API Base URL:', import.meta.env.VITE_API_BASE_URL)


export default instance

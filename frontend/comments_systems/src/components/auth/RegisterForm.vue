<template>

  <form @submit.prevent="handleRegister">
    <input v-model="username" placeholder="Username" type="text" required />
    <input v-model="email" type="email" placeholder="Email" required />
    <input v-model="homePageUrl" type="text" placeholder="Home Page URL" />
    <input v-model="password" type="password" placeholder="Password" required />
    <input v-model="confirmPassword" type="password" placeholder="Confirm Password" required />
    <button type="submit">Register</button>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/store/auth'
import { useRouter } from 'vue-router'

const username = ref('')
const email = ref('')
const password = ref('')
const auth = useAuthStore()
const router = useRouter()
const homePageUrl = ref('')
const confirmPassword = ref('')

const handleRegister = async () => {
  try {
    await auth.register({ username: username.value, email: email.value, password: password.value, password_repeat: confirmPassword.value, home_page_url: homePageUrl.value })
    router.push('/login')
  } catch (e) {
    alert('Registration failed')
  }
}
</script>

<style scoped>
form {
  max-width: 400px;
  margin: 30px auto;
  padding: 25px 30px;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  border: 1px solid #eaeaea;
  transition: box-shadow 0.3s ease, transform 0.3s ease;
}

form:hover {
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.12);
  transform: translateY(-3px);
}

h2 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 20px;
  font-size: 1.8rem;
  font-weight: 600;
}

input[type="email"],
input[type="text"],
input[type="password"] {
  width: 100%;
  padding: 12px 16px;
  margin-bottom: 18px;
  font-size: 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  background-color: #fafafa;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

input[type="email"]:focus,
input[type="text"]:focus,
input[type="password"]:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 4px rgba(52, 152, 219, 0.15);
  background-color: #fff;
}

input::placeholder {
  color: #95a5a6;
}

button {
  width: 100%;
  background-color: #2ecc71;
  color: white;
  border: none;
  padding: 14px 0;
  font-size: 1.1rem;
  font-weight: 600;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

button:hover {
  background-color: #27ae60;
  transform: translateY(-3px);
}

button:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
  transform: none;
}
</style>

<template>
    <form @submit.prevent="onSubmit" class="space-y-4">
        <input v-model="email" type="email" placeholder="Email" required class="input" />
        <input v-model="password" type="password" placeholder="Password" required class="input" />
        <button type="submit" class="btn">Login</button>
    </form>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/store/auth'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const auth = useAuthStore()
const router = useRouter()

const onSubmit = async () => {
    try {
        await auth.login({ email: email.value, password: password.value })
        router.push('/')
    } catch (error) {
        alert('Login failed')
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

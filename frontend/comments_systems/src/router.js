import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from './components/auth/LoginPage.vue'
import RegisterPage from './components/auth/RegisterPage.vue'
import CommentPage from './components/CommentPage.vue'


const routes = [
    { path: '/comments', component: CommentPage },
    { path: '/login', component: LoginPage },
    { path: '/', component: RegisterPage },
]

export default createRouter({
    history: createWebHistory(),
    routes,
})

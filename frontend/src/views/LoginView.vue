<template>
    <div class="min-h-screen w-full bg-black p-8">
        <div class=" border-gray-500 border-2 mx-auto w-160 p-4 rounded-2xl m-32">
            <h1 class="text-center text-2xl text-white">Welcome back!</h1>
            <form @submit.prevent="handleLogin">
                <input v-model="form.username" placeholder="Username" required class="mr-2 p-1 placeholder-gray-400 bg-white">
                <input v-model="form.password" type="password" placeholder="Password" required class="mr-2 p-1 placeholder-gray-400 bg-white">
                <button type="submit" class="bg-emerald-400 rounded-3xl p-1.5 m-0.5  hover:bg-emerald-600 text-white w-20">Login</button>
            </form>
            <h3 class="text-white">Don't have an account?</h3>
            <button @click="handleRegisterRedirect" class="bg-emerald-400 rounded-3xl p-1.5 m-0.5  hover:bg-emerald-600 text-white w-20">Register</button>
        </div>
    </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { ref } from 'vue'
import api from '@/auth.js'
import { useRouter } from 'vue-router'

const router = useRouter()
const form = ref({
    username: '',
    password: ''
})

onMounted(() => {
    if (localStorage.getItem('token')) {
        router.push('/feed')
    }
})

const handleRegisterRedirect = () => {
    try {
        router.push('/register')
    } catch (error) {
        alert('Register failed!')
    }
}

const handleLogin = async () => {
    try {
        const response = await api.post('login/', form.value)
        localStorage.setItem('token', response.data.access)
        router.push('/feed')
    } catch (error) {
        alert('Login failed!')
    }
}
</script>
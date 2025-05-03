<template>
    <div class="min-h-screen w-full bg-black p-8">
        <div class=" border-gray-500 border-2 mx-auto w-160 p-4 rounded-2xl m-32">
            <h1 class="text-center text-2xl text-white mb-2">Register</h1>
            <form @submit.prevent="handleRegister" class="auth-form">
                <input v-model="form.username" placeholder="Username" required class="mr-2 p-1 placeholder-gray-400 bg-white">
                <input v-model="form.password" type="password" placeholder="Password" required class="mr-2 mb-1 p-1 placeholder-gray-400 bg-white">
                <input v-model="form.first_name" placeholder="First Name" required class="mr-2 mb-1 p-1 placeholder-gray-400 bg-white">
                <input v-model="form.last_name" placeholder="Last Name" required class="mr-2 mb-1 p-1 placeholder-gray-400 bg-white">
                <textarea v-model="form.bio" placeholder="Bio (optional)" class="mr-2 mb-1 p-1 placeholder-gray-400 bg-white"></textarea>
                <input type="file" @change="handleAvatarUpload" class="mr-2 mb-1 p-1 placeholder-gray-400 bg-white hover:bg-emerald-600">
                <button class="bg-emerald-400 rounded-3xl p-1.5 m-0.5  hover:bg-emerald-600 text-white w-20">Register</button>
            </form>
        </div>
    </div>
</template>

<script setup>
import {ref, onMounted} from 'vue'
import api from '@/auth.js'
import { useRouter } from 'vue-router'

const router = useRouter()
const form = ref({
    username: '',
    password: '',
    first_name: '',
    last_name: '',
    bio: '',
    avatar: null
})

onMounted(() => {
    if (localStorage.getItem('token')) {
        router.push('/feed')
    }
})

const handleAvatarUpload = (event) => {
  form.value.avatar = event.target.files[0];
}

const handleRegister = async () => {
  const formData = new FormData();
  Object.entries(form.value).forEach(([key, value]) => {
    if (value) formData.append(key, value);
  });
  
  try {
    await api.post('register/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    router.push('/login');
  } catch (error) {
    alert(error.response?.data?.detail || 'Registration failed');
  }
}
</script>
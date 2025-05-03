<template>
    <div class="min-h-screen w-full bg-black p-8">
        <div class=" border-gray-500 border-2 mx-auto w-160 p-4 rounded-2xl m-32">
            <h1 class="text-center text-2xl text-white">How are you today?</h1>
            <h2 class="text-white">Create new post</h2>
            <form @submit.prevent="handleCreatePost" class="input-form">
                <textarea 
                    v-model="postForm.content" 
                    placeholder="What's on your mind" 
                    required 
                    class="w-full p-2 mb-2 bg-gray-800 text-white rounded">
                </textarea>
                <button 
                    type="submit"
                    class="bg-emerald-400 rounded-3xl p-1.5 hover:bg-emerald-600 text-white w-50">
                    Post
                </button>
            </form>
            <h3 class="text-white mt-5">Newest posts:</h3>
            <div v-for="post in posts" :key="post.id" class="mb-4 p-4 bg-gray-800 rounded-lg">
                <div class="flex items-center mb-2">
                    <img 
                        v-if="post.user_avatar" 
                        :src="post.user_avatar" 
                        class="w-8 h-8 rounded-full mr-2">
                    <span class="text-white font-medium">{{ post.user_first_name }}</span>
                </div>
                <p class="text-white">{{ post.content }}</p>
                <p class="text-gray-400 text-sm">
                    {{ new Date(post.created_at).toLocaleString() }}
                </p>
            </div>
            <button 
                @click="handleLogout" 
                class="mt-4 bg-red-500 rounded-3xl p-1.5 hover:bg-red-600 text-white w-50">
                Logout
            </button> 
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/auth.js'
import { useRouter } from 'vue-router'

const router = useRouter()
const posts = ref([])
const postForm = ref({
    content: ''
})

const handleLogout = async () => {
    try {
        localStorage.removeItem('token')
        router.push('/login')
    } catch (error) {
        console.error('Error logging out:', error)
    }
}

const handleCreatePost = async () => {
    try {
        const response = await api.post('posts/', postForm.value)
        posts.value.unshift(response.data)
        postForm.value.content = ''
    } catch (error) {
        alert('Failed to create Post')
    }
}

onMounted(fetchPosts)

async function fetchPosts() {
    try {
        const response = await api.get('posts/')
        posts.value = response.data.results || response.data
    } catch (error) {
        console.error('Error fetching Posts:', error)
    }
}
</script>
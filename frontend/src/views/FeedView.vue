<template>
    <div class="min-h-screen w-full bg-black p-8">

        <div class="flex justify-between items-center bg-gray-900 p-4 rounded-lg mb-6">
            <div>
                <RouterLink
                v-if="currentUserId"
                :to="{ name: 'Profile', params: { username: currentUserId } }"
                class="bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-md">
                My Profile
                </RouterLink>
            </div>

            <div class="flex items-center space-x-4">
                <button class="bg-gray-700 hover:bg-gray-600 text-white py-2 px-4 rounded-md">
                Notifications
                </button>

                <button
                @click="handleLogout"
                class="bg-red-500 hover:bg-red-600 text-white py-2 px-4 rounded-md">
                Logout
                </button>
            </div>
        </div>

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
                    <RouterLink
                        :to="{ name: 'Profile', params: { username: post.user_id} }"
                        class="text-white font-medium hover:underline">
                        <span class="text-white font-medium">{{ post.user_first_name }}</span>
                    </RouterLink>
                </div>
                <p class="text-white">{{ post.content }}</p>
                <p class="text-gray-400 text-sm">
                    {{ new Date(post.created_at).toLocaleString() }}
                </p>
                <textarea 
                    v-model="commentInputs[post.id]" 
                    placeholder="Comment..." 
                    required 
                    class="w-full p-2 mt-2 bg-gray-700 text-white rounded">
                </textarea>
                <button 
                    @click="handleCreateComment(post.id)" 
                    class="mt-2 bg-blue-600 hover:bg-blue-700 text-white py-1 px-3 rounded">
                    Submit Comment
                </button>
                <div v-if="commentsByPost[post.id]" class="mt-3">
                    <h4 class="text-white mb-1">Comments:</h4>
                    <div 
                        v-for="comment in commentsByPost[post.id]" 
                        :key="comment.id" 
                        class="p-2 mb-2 bg-gray-700 rounded text-white"
                    >
                        <div class="flex items-center mb-2">
                            <img 
                                v-if="comment.user_avatar" 
                                :src="comment.user_avatar" 
                                class="w-8 h-8 rounded-full mr-2">
                            <RouterLink
                                :to="{ name: 'Profile', params: { username: comment.user_id} }"
                                class="text-white font-medium hover:underline">
                                <span class="text-white font-medium">{{ comment.user_first_name }}</span>
                            </RouterLink>
                        </div>
                        <p class="text-sm">{{ comment.content }}</p>
                        <p class="text-xs text-gray-400">
                            {{ new Date(comment.created_at).toLocaleString() }}
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/auth.js'
import { useRouter } from 'vue-router'

const currentUserId = localStorage.getItem('user_id')
const router = useRouter()
const posts = ref([])
const postForm = ref({
    content: ''
})
const commentInputs = ref({})
const commentsByPost = ref({})

const handleLogout = async () => {
    try {
        localStorage.removeItem('token')
        localStorage.removeItem('user_id')
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

const handleCreateComment = async (postId) => {
    try {
        const content = commentInputs.value[postId]
        if (!content) return

        await api.post(`posts/${postId}/comments/`, { content })
        commentInputs.value[postId] = ''
        await fetchCommentsForPost(postId)  // refresh comment list
    } catch (error) {
        alert('Failed to create Comment')
    }
}

onMounted(fetchPosts)

async function fetchPosts() {
    try {
        const response = await api.get('posts/')
        posts.value = response.data.results || response.data

        for (const post of posts.value) {
            await fetchCommentsForPost(post.id)
        }
    } catch (error) {
        console.error('Error fetching Posts:', error)
    }
}

async function fetchCommentsForPost(postId) {
    try {
        const response = await api.get(`posts/${postId}/comments/`)
        commentsByPost.value[postId] = response.data
    } catch (error) {
        console.error(`Error fetching comments for post ${postId}:`, error)
    }
}
</script>
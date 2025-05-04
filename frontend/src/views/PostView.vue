<template>
    <NavBar />

              <div v-if="post" class="mb-4 p-4 bg-gray-800 rounded-lg">
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
  </template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/auth.js'
import NavBar from '@/components/NavBar.vue'

const route = useRoute()
const post = ref(null)
const commentInputs = ref({})
const commentsByPost = ref({})

onMounted(async () => {
    try {
        const response = await api.get(`posts/${route.params.id}/`)
        post.value = response.data
        await fetchCommentsForPost(route.params.id)
    } catch (error) {
        console.error('Error fetching Post:', error)
    }
})

async function fetchCommentsForPost(postId) {
    try {
        const response = await api.get(`posts/${postId}/comments/`)
        commentsByPost.value[postId] = response.data
    } catch (error) {
        console.error(`Error fetching comments for post ${postId}:`, error)
    }
}
</script>
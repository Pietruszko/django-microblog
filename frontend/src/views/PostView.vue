<template>
    <NavBar />
    <div class="min-h-screen w-full bg-black p-8">
      <div class="mx-auto max-w-4xl">
        <div v-if="post" class="mb-4 p-4 bg-gray-800 rounded-lg">
          <div class="flex items-center mb-2">
            <img 
              v-if="post.user_avatar" 
              :src="post.user_avatar" 
              class="w-8 h-8 rounded-full mr-2">
            <RouterLink
              :to="{ name: 'Profile', params: { username: post.user_id } }"
              class="text-white font-medium hover:underline">
              <span class="text-white font-medium">{{ post.user_first_name }}</span>
            </RouterLink>
          </div>
          <p class="text-white">{{ post.content }}</p>
          <p class="text-gray-400 text-sm">
            {{ new Date(post.created_at).toLocaleString() }}
          </p>
          
          <!-- Comment Form -->
          <textarea 
            v-model="commentInput" 
            placeholder="Comment..." 
            required 
            class="w-full p-2 mt-2 bg-gray-700 text-white rounded">
          </textarea>
          <button 
            @click="handleCreateComment(post.id)" 
            class="mt-2 bg-blue-600 hover:bg-blue-700 text-white py-1 px-3 rounded">
            Submit Comment
          </button>
          
          <!-- Comments Section -->
          <div class="mt-3">
            <h4 class="text-white mb-1">Comments:</h4>
            
            <!-- Comments List -->
            <div 
              v-for="comment in comments.results" 
              :key="comment.id" 
              class="p-2 mb-2 bg-gray-700 rounded text-white"
            >
              <div class="flex items-center mb-2">
                <img 
                  v-if="comment.user_avatar" 
                  :src="comment.user_avatar" 
                  class="w-8 h-8 rounded-full mr-2">
                <RouterLink
                  :to="{ name: 'Profile', params: { username: comment.user_id } }"
                  class="text-white font-medium hover:underline">
                  <span class="text-white font-medium">{{ comment.user_first_name }}</span>
                </RouterLink>
              </div>
              <p class="text-sm">{{ comment.content }}</p>
              <p class="text-xs text-gray-400">
                {{ new Date(comment.created_at).toLocaleString() }}
              </p>
            </div>
            
            <!-- Load More Comments -->
            <div v-if="comments.next" class="text-center mt-4">
              <button
                @click="loadMoreComments"
                :disabled="loadingComments"
                class="bg-gray-600 hover:bg-gray-500 text-white py-1 px-4 rounded"
              >
                <span v-if="loadingComments">Loading...</span>
                <span v-else>Load More Comments</span>
              </button>
            </div>
            
            <!-- Loading Indicator -->
            <div v-if="loadingComments" class="text-center py-4">
              <div class="inline-block animate-spin rounded-full h-6 w-6 border-t-2 border-b-2 border-blue-400"></div>
            </div>
            
            <!-- No Comments Message -->
            <div v-if="!loadingComments && comments.results && comments.results.length === 0" class="text-gray-400 text-center py-4">
              No comments yet
            </div>
          </div>
        </div>
        
        <!-- Post Loading Indicator -->
        <div v-if="loadingPost" class="text-center py-8">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-emerald-400"></div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, watch } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import api from '@/auth.js'
  import NavBar from '@/components/NavBar.vue'
  
  const route = useRoute()
  const router = useRouter()
  
  const post = ref(null)
  const commentInput = ref('')
  const comments = ref({
    count: 0,
    next: null,
    previous: null,
    results: []
  })
  const loadingPost = ref(false)
  const loadingComments = ref(false)
  
  // Fetch post and initial comments
  onMounted(async () => {
    await fetchPost()
    await fetchComments()
  })
  
  // Watch for route changes (like when refreshing the same post)
  watch(() => route.params.id, async (newId) => {
    if (newId) {
      await fetchPost()
      await fetchComments()
    }
  })
  
  async function fetchPost() {
    try {
      loadingPost.value = true
      const response = await api.get(`posts/${route.params.id}/`)
      post.value = response.data
    } catch (error) {
      console.error('Error fetching post:', error)
      // Redirect to feed or show error message
      router.push({ name: 'Feed' })
    } finally {
      loadingPost.value = false
    }
  }
  
  async function fetchComments(page = 1) {
    try {
      loadingComments.value = true
      const response = await api.get(`posts/${route.params.id}/comments/?page=${page}`)
      
      if (page === 1) {
        comments.value = response.data
      } else {
        comments.value = {
          ...response.data,
          results: [...comments.value.results, ...response.data.results]
        }
      }
    } catch (error) {
      console.error('Error fetching comments:', error)
    } finally {
      loadingComments.value = false
    }
  }
  
  async function loadMoreComments() {
    if (!comments.value.next || loadingComments.value) return
    
    try {
      loadingComments.value = true
      const nextPage = new URL(comments.value.next).searchParams.get('page')
      await fetchComments(parseInt(nextPage))
    } catch (error) {
      console.error('Error loading more comments:', error)
    }
  }
  
  async function handleCreateComment(postId) {
    if (!commentInput.value.trim()) return
    
    try {
      const response = await api.post(`posts/${postId}/comments/`, {
        content: commentInput.value
      })
      
      // Add new comment to the top of the list
      comments.value.results.unshift(response.data)
      comments.value.count += 1
      
      // Clear input
      commentInput.value = ''
    } catch (error) {
      console.error('Error creating comment:', error)
      alert('Failed to create comment')
    }
  }
  </script>
<template>
    <div class="min-h-screen w-full bg-black p-8">
      <NavBar />
  
      <div class="mx-auto max-w-4xl">
        <div class="border-gray-500 border-2 p-4 rounded-2xl mb-6">
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
        </div>
  
        <h3 class="text-white mb-4">Newest posts:</h3>
        
        <div class="space-y-6">
          <div 
            v-for="post in posts" 
            :key="post.id" 
            class="border-gray-500 border-2 p-4 rounded-2xl bg-gray-800">
            <div @click="goToPost(post.id)" class="cursor-pointer">
              <div class="flex items-center mb-2">
                  <img 
                    v-if="post.user_avatar" 
                    :src="post.user_avatar" 
                    @click.stop=""
                    class="w-8 h-8 rounded-full mr-2 cursor-default">
                <RouterLink
                  :to="{ name: 'Profile', params: { username: post.user_id} }"
                  @click.stop=""
                  class="text-white font-medium hover:underline">
                  <span class="text-white font-medium">{{ post.user_first_name }}</span>
                </RouterLink>
              </div>
              <p class="text-white">{{ post.content }}</p>
              <p class="text-gray-400 text-sm">
                {{ new Date(post.created_at).toLocaleString() }}
              </p>
            </div>
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
            <div v-if="commentsByPost[post.id]?.results" class="mt-3">
              <h4 class="text-white mb-1">Comments:</h4>
              <div 
                v-for="comment in commentsByPost[post.id].results" 
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
              <div v-if="commentsByPost[post.id]?.count > 5 && commentsByPost[post.id]?.results.length < commentsByPost[post.id]?.count" 
                    class="flex justify-between mt-2">
                <button
                    @click="loadMoreComments(post.id)"
                    class="text-xs text-blue-400 hover:text-blue-300"
                    :disabled="!commentsByPost[post.id]?.next || loadingComments[post.id]"
                >
                    <span v-if="loadingComments[post.id]">Loading...</span>
                    <span v-else>Load More Comments</span>
                </button>
                <span class="text-xs text-gray-400">
                    Showing {{ commentsByPost[post.id].results.length }} of {{ commentsByPost[post.id].count }}
                </span>
                </div>
            </div>
          </div>
  
          <div v-if="loading" class="text-center py-8">
            <div class="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-emerald-400"></div>
          </div>
  
          <div v-if="noMorePosts" class="text-center text-gray-400 py-8">
            No more posts to load
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, onUnmounted } from 'vue'
  import api from '@/auth.js'
  import NavBar from '@/components/NavBar.vue'
  import { useRouter } from 'vue-router'
  
  const posts = ref([])
  const postForm = ref({ content: '' })
  const commentInputs = ref({})
  const commentsByPost = ref({})
  const currentPage = ref(1)
  const totalPages = ref(1)
  const loading = ref(false)
  const loadingComments = ref({})
  const noMorePosts = ref(false)
  const router = useRouter()

  function goToPost(postId) {
    router.push({ name: 'PostDetail', params: { id: postId } })
}
  
  const handleScroll = () => {
    if (loading.value || noMorePosts.value) return

    const { scrollTop, scrollHeight, clientHeight } = document.documentElement
    const threshold = 100 // pixels from bottom

    if (scrollTop + clientHeight >= scrollHeight - threshold) {
      loadMorePosts()
    }
}
  
  async function fetchPosts() {
    try {
      loading.value = true

      const response = await api.get('posts/')
      posts.value = response.data.results
      currentPage.value = 1
      totalPages.value = Math.ceil(response.data.count / 5)
      console.log("🔍 Posts response:", response.data)

      
      
      for (const post of posts.value) {
        await fetchCommentsForPost(post.id)
      }
    } catch (error) {
      console.error('Error fetching posts:', error)
    } finally {
      loading.value = false
    }
  }
  
  
  async function loadMorePosts() {
    if (currentPage.value >= totalPages.value || loading.value) {
      noMorePosts.value = true
      return
    }

    try {
      loading.value = true
      const nextPage = currentPage.value + 1
      const response = await api.get(`posts/?page=${nextPage}`)
      
      if (response.data.results?.length) {
        // Store the new posts in a variable before assigning
        const newPosts = response.data.results
        posts.value = [...posts.value, ...newPosts]
        currentPage.value = nextPage
        
        // Fetch comments for all new posts in parallel
        await Promise.all(newPosts.map(post => fetchCommentsForPost(post.id)))
      } else {
        noMorePosts.value = true
      }
    } catch (error) {
      console.error('Error loading more posts:', error)
    } finally {
      loading.value = false
    }
}
  
  async function fetchCommentsForPost(postId, page = 1) {
    try {
      loadingComments.value[postId] = true
      const response = await api.get(`posts/${postId}/comments/?page=${page}`)
      
      if (page === 1) {
        commentsByPost.value[postId] = response.data
      } else {
        commentsByPost.value[postId] = {
          ...response.data,
          results: [...(commentsByPost.value[postId]?.results || []), ...response.data.results]
        }
      }
    } catch (error) {
      console.error(`Error fetching comments for post ${postId}:`, error)
    } finally {
      loadingComments.value[postId] = false
    }
}

const loadMoreComments = async (postId) => {
  if (!commentsByPost.value[postId]?.next) return
  
  try {
    const nextPage = commentsByPost.value[postId].next.split('page=')[1]
    await fetchCommentsForPost(postId, nextPage)
  } catch (error) {
    console.error('Error loading more comments:', error)
  }
}
  
  const handleCreatePost = async () => {
    try {
      const response = await api.post('posts/', postForm.value)
      posts.value.unshift(response.data)
      postForm.value.content = ''
      await fetchCommentsForPost(response.data.id)
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
        
        // Refresh comments - load first page to show new comment at top
        await fetchCommentsForPost(postId, 1)
    } catch (error) {
        alert('Failed to create Comment')
    }
}
  
  onMounted(() => {
  fetchPosts().then(() => {
    window.addEventListener('scroll', handleScroll)
  })
})

  
  onUnmounted(() => {
    window.removeEventListener('scroll', handleScroll)
  })
  </script>
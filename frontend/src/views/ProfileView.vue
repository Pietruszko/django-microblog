<template>
  <div class="min-h-screen bg-black text-white p-4">
    <NavBar />

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-8">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-emerald-400"></div>
    </div>

    <!-- Profile Content -->
    <div v-if="profile" class="max-w-2xl mx-auto">
      <!-- Profile Header Section -->
      <div class="flex items-center gap-4 mb-6">
        <img 
          :src="profile.avatar || '/default-avatar.png'" 
          class="w-40 h-40 rounded-full object-cover border-2 border-emerald-400"
        >
        <div>
          <h1 class="text-2xl font-bold">
            {{ profile.first_name }} {{ profile.last_name }}
          </h1>
        </div>
      </div>
      
      <!-- Bio Section -->
      <div class="bg-gray-800 p-4 rounded-lg mb-6">
        <div v-if="editMode" class="mb-4">
          <textarea
            v-model="editBio"
            class="w-full p-2 mb-2 bg-gray-700 text-white rounded"
            rows="4"
            placeholder="Tell us about yourself"
          ></textarea>
          <div class="flex space-x-2">
            <button
              @click="saveBio"
              class="bg-emerald-500 hover:bg-emerald-600 px-4 py-2 rounded"
            >
              Save Changes
            </button>
            <button
              @click="editMode = false"
              class="bg-gray-500 hover:bg-gray-600 px-4 py-2 rounded"
            >
              Cancel
            </button>
          </div>
        </div>
        <div v-else>
          <p v-if="profile.bio">{{ profile.bio }}</p>
          <p v-else class="text-gray-400">No bio yet</p>
          <button 
            v-if="isOwnProfile"
            @click="editMode = true"
            class="mt-2 bg-emerald-500 hover:bg-emerald-600 px-4 py-2 rounded text-sm"
          >
            Edit Bio
          </button>
        </div>
      </div>

      <!-- User Posts Section -->
      <div class="mb-8">
        <h2 class="text-xl font-bold mb-4">Posts</h2>
        
        <!-- Posts List -->
        <div v-if="profile.posts.length" class="space-y-4">
          <div 
            v-for="post in profile.posts" 
            :key="post.id" 
            class="border border-gray-700 rounded-lg p-4 bg-gray-800"
          >
          <div @click="goToPost(post.id)" class="cursor-pointer">
            <p class="text-white">{{ post.content }}</p>
            <p class="text-gray-400 text-sm mt-2">
              {{ new Date(post.created_at).toLocaleString() }}
            </p>
          </div>
          </div>
        </div>
        
        <div v-else class="text-center py-8 text-gray-400">
          No posts yet
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/auth.js'
import NavBar from '@/components/NavBar.vue'

const route = useRoute()
const router = useRouter()

// Profile data
const profile = ref(null)
const loading = ref(true)
const editMode = ref(false)
const editBio = ref('')

function goToPost(postId) {
    router.push({ name: 'PostDetail', params: { id: postId } })
}

const isOwnProfile = computed(() => {
  const userId = parseInt(localStorage.getItem('user_id'))
  return userId && userId === profile.value.user_id
})

async function fetchProfile() {
  try {
    loading.value = true
    const response = await api.get(`profiles/${route.params.username}/`)
    profile.value = response.data
  } catch (err) {
    console.error('Profile fetch error:', err)
    if (err.response?.status === 401) router.push('/login')
  } finally {
    loading.value = false
  }
}

const saveBio = async () => {
  try {
    loading.value = true
    const userId = localStorage.getItem('user_id')
    if (!userId) throw new Error('User ID not found')

    await api.patch(`profiles/${userId}/`, { bio: editBio.value })
    
    profile.value.bio = editBio.value
    editMode.value = false
  } catch (error) {
    console.error('Save bio error:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchProfile()
})
</script>
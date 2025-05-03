<template>
    <div class="min-h-screen bg-black text-white p-4">
      <!-- Loading State -->
      <div v-if="loading" class="text-center py-8">
        Loading profile...
      </div>
  
      <!-- Error State -->
      <div v-if="error" class="text-red-500 text-center py-8">
        Error loading profile: {{ error }}
      </div>
  
      <!-- Profile Content -->
      <div v-if="profile" class="max-w-2xl mx-auto">
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
  
        <div class="bg-gray-800 p-4 rounded-lg mb-6">
          <p v-if="profile.bio">{{ profile.bio }}</p>
          <p v-else class="text-gray-400">No bio yet</p>
        </div>
  
        <button 
          v-if="isOwnProfile"
          @click="editMode = !editMode"
          class="bg-emerald-500 hover:bg-emerald-600 px-4 py-2 rounded"
        >
          {{ editMode ? 'Cancel' : 'Edit Profile' }}
        </button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, onMounted } from 'vue'
  import { useRoute } from 'vue-router'
  import api from '@/auth.js'
  
  const route = useRoute()
  const profile = ref(null)
  const loading = ref(true)
  const error = ref(null)
  const editMode = ref(false)
  
  const isOwnProfile = computed(() => {
    return profile.value?.user?.username === localStorage.getItem('username')
  })
  
async function fetchProfile() {
  try {
    loading.value = true
    let apiUrl = `profiles/${route.params.username}/`

    const response = await api.get(apiUrl)
    profile.value = response.data
  } catch (err) {
    if (err.response?.status === 401) {
      // Handle unauthorized (not logged in)
      router.push('/login')
    }
    error.value = err.response?.data?.detail || err.message
  } finally {
    loading.value = false
  }
}
  
  onMounted(fetchProfile)
  </script>
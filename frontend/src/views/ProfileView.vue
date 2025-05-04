<template>
    <div class="min-h-screen bg-black text-white p-4">

      <NavBar />

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
        
        <div v-if="editMode" class="mt-4 bg-gray-800 p-4 rounded-lg">
          <h3 class="text-lg font-bold mb-2">Edit Bio</h3>
          <textarea
            v-model="editBio"
            class="w-full p-2 mb-2 bg-gray-700 text-white rounded"
            rows="4"
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

        <div class="bg-gray-800 p-4 rounded-lg mb-6">
          <p v-if="profile.bio">{{ profile.bio }}</p>
          <p v-else class="text-gray-400">No bio yet</p>
        </div>
  
        <button 
          v-if="profile && isOwnProfile"
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
  import { useRoute, useRouter } from 'vue-router'
  import api from '@/auth.js'
  import NavBar from '@/components/NavBar.vue'
  
  const route = useRoute()
  const router = useRouter()
  const profile = ref(null)
  const loading = ref(true)
  const error = ref(null)
  const editMode = ref(false)
  const editBio = ref('')
  
  
  const isOwnProfile = computed(() => {
    const userId = parseInt(localStorage.getItem('user_id'))
    const routeId = parseInt(route.params.username)  // despite being called username
    return userId && routeId && userId === routeId
  })
  
  async function fetchProfile() {
    try {
      console.log('Fetching profile for:', route.params.username)
      loading.value = true
      error.value = null
      
      const apiUrl = `profiles/${route.params.username}/`
      const response = await api.get(apiUrl)
      
      console.log('Profile API response:', response.data)
      profile.value = response.data
      editBio.value = response.data.bio || ''
      
    } catch (err) {
      console.error('Profile fetch error:', err)
      error.value = err.response?.data?.detail || err.message || 'Failed to load profile'
      
      if (err.response?.status === 401) {
        router.push('/login')
      }
    } finally {
      loading.value = false
      console.log('Fetch completed', { profile: profile.value, error: error.value })
    }
  }
  
  const saveBio = async () => {
    try {
      loading.value = true
      const userId = localStorage.getItem('user_id')
      if (!userId) throw new Error('User ID not found')

      console.log('Saving bio:', editBio.value)

      await api.patch(`profiles/${userId}/`, { bio: editBio.value })
      
      profile.value.bio = editBio.value
      editMode.value = false
    } catch (error) {
      console.error('Save bio error:', error)
      error.value = error.response?.data?.detail || 'Failed to update bio. Please try again.'
    } finally {
      loading.value = false
    }
  }

  
  onMounted(() => {
    console.log('Component mounted')
    fetchProfile()
  })
  </script>
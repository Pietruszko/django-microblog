<template>
    <div class="flex justify-between items-center bg-gray-900 p-4 rounded-lg mb-6">
      <!-- Left Side -->
      <div>
        <RouterLink
          v-if="currentUserId"
          :to="{ name: 'Profile', params: { username: currentUserId } }"
          class="bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-md"
        >
          My Profile
        </RouterLink>
      </div>
      <div>
        <RouterLink
          v-if="currentUserId"
          :to="{ name: 'Feed' }"
          class="bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-md"
        >
          Django-Microblog
        </RouterLink>
      </div>
  
      <!-- Right Side -->
      <div class="flex items-center space-x-4">
        <button class="bg-gray-700 hover:bg-gray-600 text-white py-2 px-4 rounded-md">
          Notifications
        </button>
  
        <button
          @click="handleLogout"
          class="bg-red-500 hover:bg-red-600 text-white py-2 px-4 rounded-md"
        >
          Logout
        </button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { useRouter } from 'vue-router'
  
  const router = useRouter()
  const currentUserId = localStorage.getItem('user_id')
  
  const handleLogout = async () => {
    try {
      await api.post('logout/') // If you have logout endpoint
      localStorage.removeItem('token')
      localStorage.removeItem('user_id')
      router.push('/login')
    } catch (error) {
      console.error('Error logging out:', error)
    }
  }
  </script>
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
      
      <!-- Center - Moved Django-Microblog here -->
      <div>
        <RouterLink
          :to="{ name: 'Feed' }"
          class="bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-md"
        >
          Django-Microblog
        </RouterLink>
      </div>
  
      <!-- Right Side -->
      <div class="flex items-center space-x-4">
        <!-- Notifications Button and Dropdown -->
        <div class="relative" ref="notificationsDropdown">
          <button 
            @click.stop="toggleNotifications"
            class="bg-gray-700 hover:bg-gray-600 text-white py-2 px-4 rounded-md"
          >
            Notifications
          </button>
  
          <div 
            v-if="showNotifications"
            class="absolute right-0 mt-2 w-64 bg-gray-800 rounded-md shadow-lg z-50"
          >
            <div class="p-4">
              <div class="flex justify-between items-center mb-2">
                <h3 class="text-white font-bold">Notifications</h3>
                <button @click.stop="closeNotifications" class="text-gray-400 hover:text-white">
                  ✕
                </button>
              </div>
                <div class="divide-y divide-gray-700">
                    <div 
                        v-for="notification in notifications" 
                        :key="notification.id" 
                        class="p-2 hover:bg-gray-700 cursor-pointer"
                        @click="handleNotificationClick(notification)"
                    >
                        <p class="text-sm text-white">{{ notification.message }}</p>
                        <p class="text-xs text-gray-400">
                            {{ new Date(notification.created_at).toLocaleString() }}
                        </p>
                    </div>
                    <div v-if="notifications.length === 0" class="p-2 text-gray-400 text-sm">
                        No new notifications
                    </div>
                </div>
            </div>
          </div>
        </div>
  
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
  import { ref, onMounted, onUnmounted } from 'vue'
  import { useRouter } from 'vue-router'
  import api from '@/auth.js'
  
  const router = useRouter()
  const currentUserId = localStorage.getItem('user_id')
  const showNotifications = ref(false)
  const notificationsDropdown = ref(null)
  const notifications = ref([])
  
  // Handle click outside to close notifications
  const handleClickOutside = (event) => {
    if (notificationsDropdown.value && !notificationsDropdown.value.contains(event.target)) {
      closeNotifications()
    }
  }
  
  // Set up event listeners
  onMounted(() => {
    document.addEventListener('click', handleClickOutside)
  })
  
  onUnmounted(() => {
    document.removeEventListener('click', handleClickOutside)
  })
  
  const toggleNotifications = (event) => {
    event?.stopPropagation()
    showNotifications.value = !showNotifications.value
  }
  
  const closeNotifications = () => {
    showNotifications.value = false
  }
  
  const handleLogout = async () => {
    try {
      localStorage.removeItem('token')
      localStorage.removeItem('user_id')
      router.push('/login')
    } catch (error) {
      console.error('Error logging out:', error)
    }
  }

  onMounted(fetchNotifications)

  async function fetchNotifications() {
    try {
        const response = await api.get('notifications/')
        notifications.value = response.data.results || response.data
    } catch (error) {
        console.error('Error fetching Notifications:', error)
    }
}
  </script>
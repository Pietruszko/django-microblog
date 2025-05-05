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

              <!-- Action Buttons -->
              <div class="flex space-x-2 mb-3">
                <button 
                  @click.stop="markAllAsRead"
                  class="text-xs bg-blue-600 hover:bg-blue-700 text-white px-2 py-1 rounded"
                  :disabled="notifications.length === 0 || notifications.every(n => n.is_read)"
                >
                  Mark All Read
                </button>
                <button 
                  @click.stop="deleteAllNotifications"
                  class="text-xs bg-red-600 hover:bg-red-700 text-white px-2 py-1 rounded"
                  :disabled="notifications.length === 0"
                >
                  Delete All
                </button>
              </div>
              
              <!-- Notifications List -->

                <div class="divide-y divide-gray-700 max-h-64 overflow-y-auto">
                  <div 
                    v-for="notification in notifications" 
                    :key="notification.id" 
                    class="p-2 hover:bg-gray-700 transition-colors duration-200 relative group"
                    :class="{
                      'bg-gray-700 border-l-2 border-blue-500': !notification.is_read,
                      'bg-gray-800': notification.is_read
                    }"
                  >
                    <!-- Notification Content (clickable area) -->
                    <div 
                      class="cursor-pointer pr-6" 
                      @click="handleNotificationClick(notification)"
                    >
                      <p class="text-sm text-white">{{ notification.message }}</p>
                      <p class="text-xs text-gray-400">
                        {{ new Date(notification.created_at).toLocaleString() }}
                      </p>
                    </div>

                    <!-- Delete Button (positioned absolutely) -->
                    <button 
                      @click.stop="deleteNotification(notification)"
                      class="absolute right-2 top-2 text-gray-400 hover:text-white opacity-0 group-hover:opacity-100 transition-opacity"
                    >
                      ✕
                    </button>
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
  const loading = ref(false)
  
  
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
  
  const toggleNotifications = async (event) => {
    event?.stopPropagation()
    showNotifications.value = !showNotifications.value
    if (showNotifications.value) {
      await fetchNotifications()
    }
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
  
  const handleNotificationClick = async (notification) => {
  try {
    // Mark as read if needed
    if (!notification.is_read) {
      await api.patch(`notifications/${notification.id}/`, { is_read: true })
    }

    // Check if we're already viewing this post
    const currentPostId = router.currentRoute.value.params.id
    const isSamePost = currentPostId === String(notification.post_id)

    if (isSamePost) {
      await router.push({
        name: 'PostDetail',
        params: { id: notification.post_id },
        query: { refresh: Date.now() } // Unique value forces update
      })
    } else {
      // Normal navigation for different posts
      await router.push({
        name: 'PostDetail', 
        params: { id: notification.post_id }
      })
    }

    closeNotifications()
    await fetchNotifications()
  } catch (error) {
    console.error('Error handling notification:', error)
  }
}
  
  async function fetchNotifications() {
    try {
      loading.value = true
      const response = await api.get('notifications/')
      notifications.value = response.data.results || response.data
    } catch (error) {
      console.error('Error fetching Notifications:', error)
    } finally {
      loading.value = false
    }
  }

  const deleteNotification = async (notification) => {
  try {
    await api.delete(`notifications/${notification.id}/`)
    notifications.value = notifications.value.filter(n => n.id !== notification.id)
  } catch (error) {
    console.error('Error deleting notification:', error)
    alert('Failed to delete notification')
  }
}

const markAllAsRead = async () => {
  try {
    await api.post('notifications/mark_all_read/')
    // Update local state
    notifications.value = notifications.value.map(n => ({ ...n, is_read: true }))
  } catch (error) {
    console.error('Error marking all as read:', error)
    alert('Failed to mark all as read')
  }
}

const deleteAllNotifications = async () => {
  if (!confirm('Are you sure you want to delete all notifications?')) return
  
  try {
    await api.delete('notifications/delete_all/')
    notifications.value = [] // Clear local state
  } catch (error) {
    console.error('Error deleting all notifications:', error)
    alert('Failed to delete all notifications')
  }
}
  </script>
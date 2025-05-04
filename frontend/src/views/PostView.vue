<template>
    <NavBar />
    <div v-if="post" class="text-white p-4">
      <h1 class="text-xl font-bold mb-2">{{ post.content }}</h1>
      <!-- Optionally display comments, author, etc. -->
    </div>
  </template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/auth.js'
import NavBar from '@/components/NavBar.vue'

const route = useRoute()
const post = ref(null)

onMounted(async () => {
    try {
        const response = await api.get(`posts/${route.params.id}/`)
        post.value = response.data
    } catch (error) {
        console.error('Error fetching Post:', error)
    }
})
</script>
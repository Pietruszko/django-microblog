import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import FeedView from '../views/FeedView.vue'
import RegisterView from '../views/RegisterView.vue'
import ProfileView from '@/views/ProfileView.vue'
import PostView from '@/views/PostView.vue'

const routes = [
  {
    path: '/',
    redirect: 'login'
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
    meta: { forGuestOnly: true }
  },
  {
    path: '/feed',
    name: 'Feed',
    component: FeedView,
    meta: { requiresAuth: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterView,
    meta: { forGuestOnly: true }
  },
  {
    path: '/profile/:username',
    name: 'Profile',
    component: ProfileView,
    meta: { requiresAuth: false }
  },
  {
    path: '/posts/:id',
    name: 'PostDetail',
    component: PostView,
    meta: { requiresAuth: false }
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('token')
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else if (to.meta.forGuestOnly && isAuthenticated) {
    next('/feed')
  } 
  next()
})

export default router

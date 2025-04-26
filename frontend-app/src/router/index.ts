import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
      {
        path: '/',
        name: 'home',
        component: () => import('../views/HomeView.vue'),
      },
      {
        path: '/chat',
        name: 'chat',
        component: () => import('../views/ChatView.vue'),
      },
      {
        path: '/preferences',
        name: 'preferences',
        component: () => import('../views/PreferencesView.vue'),
      },
      {
        path: '/liked',
        name: 'liked',
        component: () => import('../views/LikeHistoryView.vue'),
      }
    ],
  })
  
  export default router
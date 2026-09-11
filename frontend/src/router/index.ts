import { createRouter, createWebHistory } from 'vue-router'

import { useUserStore } from '@/stores/user'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
      meta: { public: true },
    },
    {
      path: '/',
      redirect: () => {
        const user = useUserStore()
        return user.isLoggedIn ? user.homePath : '/login'
      },
    },
    {
      path: '/home',
      name: 'home',
      component: () => import('@/views/HomeView.vue'),
      meta: { role: 'student' },
    },
    {
      path: '/chat',
      name: 'chat',
      component: () => import('@/views/ChatView.vue'),
      meta: { role: 'student' },
    },
    {
      path: '/kg',
      name: 'kg',
      component: () => import('@/views/KnowledgeGraphView.vue'),
      meta: { role: 'student' },
    },
    {
      path: '/records',
      name: 'records',
      component: () => import('@/views/RecordsView.vue'),
      meta: { role: 'student' },
    },
    {
      path: '/practice',
      name: 'practice',
      component: () => import('@/views/PracticeView.vue'),
      meta: { role: 'student' },
    },
    { path: '/exam', redirect: '/practice' },
    { path: '/exam/:id', redirect: '/practice' },
    { path: '/teacher', redirect: '/admin/class' },
    {
      path: '/teacher/:tab',
      redirect: (to) => {
        const tab = String(to.params.tab || 'class')
        const allowed = ['class', 'bank', 'learning', 'reflow', 'observe', 'config']
        const key = allowed.includes(tab) ? (tab === 'config' ? 'observe' : tab) : 'class'
        return `/admin/${key}`
      },
    },
    { path: '/admin', redirect: '/admin/class' },
    { path: '/admin/config', redirect: '/admin/observe' },
    {
      path: '/admin/:tab(class|bank|learning|reflow|observe)',
      name: 'admin',
      component: () => import('@/views/admin/AdminDashboard.vue'),
      meta: { role: 'admin' },
    },
  ],
})

router.beforeEach((to) => {
  const user = useUserStore()
  if (to.meta.public) {
    if (user.isLoggedIn && to.name === 'login') return user.homePath
    return true
  }
  if (!user.isLoggedIn) {
    return {
      path: '/login',
      query: { redirect: to.fullPath },
    }
  }
  const requiredRole = to.meta.role as string | undefined
  if (requiredRole === 'student' && user.isAdmin) return '/admin/class'
  if (requiredRole === 'admin' && user.isStudent) return '/home'
  return true
})

export default router

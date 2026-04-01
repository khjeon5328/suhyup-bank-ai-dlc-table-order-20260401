import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue'),
    meta: { requiresAuth: false },
  },
  {
    path: '/',
    component: () => import('@/components/layout/AppLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: () => import('@/views/DashboardView.vue'),
      },
      {
        path: 'menus',
        name: 'MenuManage',
        component: () => import('@/views/MenuManageView.vue'),
        meta: { requiresOwner: true },
      },
      {
        path: 'users',
        name: 'UserManage',
        component: () => import('@/views/UserManageView.vue'),
        meta: { requiresOwner: true },
      },
      {
        path: 'tables',
        name: 'TableManage',
        component: () => import('@/views/TableManageView.vue'),
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

let isInitialized = false

router.beforeEach(async (to, _from, next) => {
  const authStore = useAuthStore()

  if (!isInitialized) {
    isInitialized = true
    // authStore uses pinia-plugin-persistedstate, state is auto-restored
  }

  if (to.path === '/login' && authStore.isAuthenticated) {
    return next('/')
  }

  if (to.meta.requiresAuth !== false && !authStore.isAuthenticated) {
    return next('/login')
  }

  if (to.meta.requiresOwner && !authStore.isOwner) {
    return next('/')
  }

  next()
})

router.onError((error) => {
  if (
    error.message.includes('Failed to fetch dynamically imported module') ||
    error.message.includes('Importing a module script failed')
  ) {
    window.location.reload()
  }
})

export default router

import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/authStore'

const routes = [
  { path: '/login', name: 'Login', component: () => import('../views/LoginView.vue') },
  { path: '/', name: 'Dashboard', component: () => import('../views/DashboardView.vue'), meta: { requiresAuth: true } },
  { path: '/menus', name: 'MenuManage', component: () => import('../views/MenuManageView.vue'), meta: { requiresAuth: true, ownerOnly: true } },
  { path: '/tables', name: 'TableManage', component: () => import('../views/TableManageView.vue'), meta: { requiresAuth: true } },
  { path: '/users', name: 'UserManage', component: () => import('../views/UserManageView.vue'), meta: { requiresAuth: true, ownerOnly: true } },
]

const router = createRouter({ history: createWebHistory(), routes })

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isAuthenticated) return { name: 'Login' }
  if (to.meta.ownerOnly && auth.role !== 'owner') return { name: 'Dashboard' }
})

export default router
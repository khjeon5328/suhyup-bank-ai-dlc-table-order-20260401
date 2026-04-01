import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/authStore'

const routes = [
  { path: '/setup', name: 'Setup', component: () => import('../views/LoginSetupView.vue') },
  { path: '/', name: 'Menu', component: () => import('../views/MenuView.vue'), meta: { requiresAuth: true } },
  { path: '/cart', name: 'Cart', component: () => import('../views/CartView.vue'), meta: { requiresAuth: true } },
  { path: '/order/confirm', name: 'OrderConfirm', component: () => import('../views/OrderConfirmView.vue'), meta: { requiresAuth: true } },
  { path: '/order/result/:orderId', name: 'OrderResult', component: () => import('../views/OrderResultView.vue'), meta: { requiresAuth: true }, props: true },
  { path: '/orders', name: 'OrderHistory', component: () => import('../views/OrderHistoryView.vue'), meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to) => {
  const authStore = useAuthStore()
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return { name: 'Setup' }
  }
})

export default router
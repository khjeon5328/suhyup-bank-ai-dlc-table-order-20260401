import { defineStore } from 'pinia'
import { orderService } from '../services/orderService'
import { sseService } from '../services/sseService'
import { useAuthStore } from './authStore'
import { useCartStore } from './cartStore'

export const useOrderStore = defineStore('order', {
  state: () => ({
    currentOrders: [],
    isLoading: false,
    sseConnected: false,
    sseConnectionLost: false
  }),
  actions: {
    async createOrder() {
      const authStore = useAuthStore()
      const cartStore = useCartStore()
      this.isLoading = true
      try {
        const data = await orderService.createOrder(
          authStore.storeId, cartStore.items
        )
        cartStore.clearCart()
        if (data.session_id) authStore.updateSessionId(data.session_id)
        return data
      } finally {
        this.isLoading = false
      }
    },
    async fetchOrders(page = 1) {
      const authStore = useAuthStore()
      this.isLoading = true
      try {
        const data = await orderService.getOrders(authStore.storeId, page)
        this.currentOrders = data
        return data
      } finally {
        this.isLoading = false
      }
    },
    updateOrderStatus(orderId, status) {
      const order = this.currentOrders.find(o => o.id === orderId)
      if (order) order.status = status
    },
    connectSSE() {
      const authStore = useAuthStore()
      if (!authStore.isAuthenticated || this.sseConnected) return

      sseService.on('order_status_changed', (data) => {
        this.updateOrderStatus(data.order_id, data.status)
      })
      sseService.on('session_ended', () => {
        const cartStore = useCartStore()
        cartStore.clearCart()
        this.currentOrders = []
      })
      sseService.onMaxRetriesExceeded = () => {
        this.sseConnectionLost = true
      }
      sseService.connect(authStore.storeId, authStore.tableId)
      this.sseConnected = true
    },
    disconnectSSE() {
      sseService.disconnect()
      this.sseConnected = false
    }
  }
})
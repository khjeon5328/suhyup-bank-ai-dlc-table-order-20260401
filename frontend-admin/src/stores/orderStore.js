import { defineStore } from 'pinia'
import { orderService } from '../services/orderService'
import { sseService } from '../services/sseService'
import { useAuthStore } from './authStore'

export const useOrderStore = defineStore('adminOrder', {
  state: () => ({ orders: [], isLoading: false, sseConnected: false, sseConnectionLost: false }),
  getters: {
    ordersByTable: (s) => {
      const map = {}
      s.orders.forEach(o => {
        if (!map[o.table_id]) map[o.table_id] = { tableId: o.table_id, orders: [], totalAmount: 0 }
        map[o.table_id].orders.push(o)
        map[o.table_id].totalAmount += o.total_amount
      })
      return Object.values(map)
    }
  },
  actions: {
    async fetchOrders() {
      const auth = useAuthStore()
      this.isLoading = true
      try { this.orders = await orderService.getOrders(auth.storeCode) } finally { this.isLoading = false }
    },
    async updateStatus(orderId, status) {
      const auth = useAuthStore()
      return await orderService.updateStatus(auth.storeCode, orderId, status)
    },
    async deleteOrder(orderId) {
      const auth = useAuthStore()
      await orderService.deleteOrder(auth.storeCode, orderId)
      this.orders = this.orders.filter(o => o.id !== orderId)
    },
    addOrder(order) { this.orders.unshift(order) },
    updateOrderInList(orderId, status) {
      const o = this.orders.find(o => o.id === orderId)
      if (o) o.status = status
    },
    removeOrderFromList(orderId) { this.orders = this.orders.filter(o => o.id !== orderId) },
    connectSSE() {
      const auth = useAuthStore()
      if (!auth.isAuthenticated || this.sseConnected) return
      sseService.on('order_created', (d) => this.addOrder(d.data || d))
      sseService.on('order_status_changed', (d) => this.updateOrderInList(d.order_id, d.new_status))
      sseService.on('order_deleted', (d) => this.removeOrderFromList(d.order_id))
      sseService.onMaxRetriesExceeded = () => { this.sseConnectionLost = true }
      sseService.connect(auth.storeCode)
      this.sseConnected = true
    },
    disconnectSSE() { sseService.disconnect(); this.sseConnected = false }
  }
})
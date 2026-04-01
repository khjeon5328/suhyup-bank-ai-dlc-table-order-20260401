import { defineStore } from 'pinia'
import { orderService } from '../services/orderService'
import { tableService } from '../services/tableService'
import { sseService } from '../services/sseService'
import { useAuthStore } from './authStore'

export const useOrderStore = defineStore('adminOrder', {
  state: () => ({ orders: [], tables: [], isLoading: false, sseConnected: false, sseConnectionLost: false }),
  getters: {
    ordersByTable: (s) => {
      // Build map from orders
      const map = {}
      s.orders.forEach(o => {
        const key = o.table_no
        if (!map[key]) map[key] = { tableNo: key, orders: [], totalAmount: 0 }
        map[key].orders.push(o)
        map[key].totalAmount += o.total_amount
      })
      // Ensure all tables are included (even without orders)
      s.tables.forEach(t => {
        if (!map[t.table_no]) map[t.table_no] = { tableNo: t.table_no, orders: [], totalAmount: 0 }
      })
      return Object.values(map).sort((a, b) => a.tableNo - b.tableNo)
    }
  },
  actions: {
    async fetchOrders() {
      const auth = useAuthStore()
      this.isLoading = true
      try {
        const [orders, tables] = await Promise.all([
          orderService.getOrders(auth.storeCode),
          tableService.getTables(auth.storeCode),
        ])
        this.orders = orders
        this.tables = tables
      } finally { this.isLoading = false }
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

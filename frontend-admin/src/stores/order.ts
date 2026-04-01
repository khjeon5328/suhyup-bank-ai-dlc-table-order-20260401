import { ref } from 'vue'
import { defineStore } from 'pinia'
import { orderApi } from '@/services/orderApi'
import type { Order, OrderHistory, OrderStatus } from '@/types/order'
import type { SSEEvent, SSEOrderCreatedData, SSEOrderStatusChangedData, SSEOrderDeletedData } from '@/types/sse'
import { SSEEventType } from '@/types/sse'

export const useOrderStore = defineStore('order', () => {
  const ordersByTable = ref<Map<number, Order[]>>(new Map())
  const orderHistory = ref<OrderHistory[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchOrders(storeId: number, tableId?: number): Promise<void> {
    loading.value = true
    error.value = null
    try {
      const response = await orderApi.getOrders(storeId, tableId)
      const orders = response.data
      // Group orders by tableId
      const grouped = new Map<number, Order[]>()
      orders.forEach((order) => {
        if (!grouped.has(order.tableId)) {
          grouped.set(order.tableId, [])
        }
        grouped.get(order.tableId)!.push(order)
      })
      if (tableId) {
        ordersByTable.value.set(tableId, grouped.get(tableId) || [])
      } else {
        ordersByTable.value = grouped
      }
    } catch (e: unknown) {
      error.value = (e as Error).message
    } finally {
      loading.value = false
    }
  }

  async function updateOrderStatus(storeId: number, orderId: number, status: OrderStatus): Promise<void> {
    const response = await orderApi.updateStatus(storeId, orderId, status)
    const updatedOrder = response.data
    const tableOrders = ordersByTable.value.get(updatedOrder.tableId)
    if (tableOrders) {
      const index = tableOrders.findIndex((o) => o.id === orderId)
      if (index !== -1) {
        tableOrders[index] = updatedOrder
      }
    }
  }

  async function deleteOrder(storeId: number, orderId: number): Promise<void> {
    await orderApi.deleteOrder(storeId, orderId)
    // Remove from local state
    for (const [tableId, orders] of ordersByTable.value.entries()) {
      const index = orders.findIndex((o) => o.id === orderId)
      if (index !== -1) {
        orders.splice(index, 1)
        if (orders.length === 0) {
          ordersByTable.value.delete(tableId)
        }
        break
      }
    }
  }

  async function fetchOrderHistory(storeId: number, tableId: number, dateFrom?: string, dateTo?: string): Promise<void> {
    loading.value = true
    error.value = null
    try {
      const response = await orderApi.getHistory(storeId, tableId, dateFrom, dateTo)
      orderHistory.value = response.data
    } catch (e: unknown) {
      error.value = (e as Error).message
    } finally {
      loading.value = false
    }
  }

  function handleSSEEvent(event: SSEEvent): void {
    switch (event.type) {
      case SSEEventType.ORDER_CREATED: {
        const data = event.data as SSEOrderCreatedData
        const order = data.order
        if (!ordersByTable.value.has(order.tableId)) {
          ordersByTable.value.set(order.tableId, [])
        }
        ordersByTable.value.get(order.tableId)!.push(order)
        break
      }
      case SSEEventType.ORDER_STATUS_CHANGED: {
        const data = event.data as SSEOrderStatusChangedData
        const tableOrders = ordersByTable.value.get(data.tableId)
        if (tableOrders) {
          const order = tableOrders.find((o) => o.id === data.orderId)
          if (order) {
            order.status = data.status as OrderStatus
          }
        }
        break
      }
      case SSEEventType.ORDER_DELETED: {
        const data = event.data as SSEOrderDeletedData
        const tableOrders = ordersByTable.value.get(data.tableId)
        if (tableOrders) {
          const index = tableOrders.findIndex((o) => o.id === data.orderId)
          if (index !== -1) {
            tableOrders.splice(index, 1)
          }
        }
        break
      }
    }
  }

  function $reset(): void {
    ordersByTable.value = new Map()
    orderHistory.value = []
    loading.value = false
    error.value = null
  }

  return {
    ordersByTable,
    orderHistory,
    loading,
    error,
    fetchOrders,
    updateOrderStatus,
    deleteOrder,
    fetchOrderHistory,
    handleSSEEvent,
    $reset,
  }
})

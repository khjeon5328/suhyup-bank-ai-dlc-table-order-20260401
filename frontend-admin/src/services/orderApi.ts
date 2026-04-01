import apiClient from './apiClient'
import type { ApiResponse } from '@/types/api'
import type { Order, OrderHistory, OrderStatus } from '@/types/order'

export const orderApi = {
  getOrders(storeId: number, tableId?: number): Promise<ApiResponse<Order[]>> {
    const params = tableId ? { tableId } : {}
    return apiClient.get(`/stores/${storeId}/orders`, { params }).then((res) => res.data)
  },

  getOrder(storeId: number, orderId: number): Promise<ApiResponse<Order>> {
    return apiClient.get(`/stores/${storeId}/orders/${orderId}`).then((res) => res.data)
  },

  updateStatus(storeId: number, orderId: number, status: OrderStatus): Promise<ApiResponse<Order>> {
    return apiClient.patch(`/stores/${storeId}/orders/${orderId}/status`, { status }).then((res) => res.data)
  },

  deleteOrder(storeId: number, orderId: number): Promise<ApiResponse<null>> {
    return apiClient.delete(`/stores/${storeId}/orders/${orderId}`).then((res) => res.data)
  },

  getHistory(storeId: number, tableId: number, dateFrom?: string, dateTo?: string): Promise<ApiResponse<OrderHistory[]>> {
    const params: Record<string, string> = {}
    if (dateFrom) params.dateFrom = dateFrom
    if (dateTo) params.dateTo = dateTo
    return apiClient.get(`/stores/${storeId}/tables/${tableId}/history`, { params }).then((res) => res.data)
  },
}

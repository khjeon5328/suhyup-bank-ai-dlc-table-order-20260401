import apiClient from './apiClient'

export const orderService = {
  async getOrders(storeId) {
    const { data } = await apiClient.get(`/stores/${storeId}/orders`)
    return data
  },
  async getOrder(storeId, orderId) {
    const { data } = await apiClient.get(`/stores/${storeId}/orders/${orderId}`)
    return data
  },
  async updateStatus(storeId, orderId, status) {
    const { data } = await apiClient.patch(`/stores/${storeId}/orders/${orderId}/status`, { status })
    return data
  },
  async deleteOrder(storeId, orderId) {
    await apiClient.delete(`/stores/${storeId}/orders/${orderId}`)
  }
}
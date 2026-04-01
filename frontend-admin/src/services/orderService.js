import apiClient from './apiClient'

export const orderService = {
  async getOrders(storeCode) {
    const { data } = await apiClient.get(`/stores/${storeCode}/orders`)
    return data
  },
  async getOrder(storeCode, orderId) {
    const { data } = await apiClient.get(`/stores/${storeCode}/orders/${orderId}`)
    return data
  },
  async updateStatus(storeCode, orderId, status) {
    const { data } = await apiClient.patch(`/stores/${storeCode}/orders/${orderId}/status`, { status })
    return data
  },
  async deleteOrder(storeCode, orderId) {
    await apiClient.delete(`/stores/${storeCode}/orders/${orderId}`)
  }
}
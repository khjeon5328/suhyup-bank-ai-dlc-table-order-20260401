import apiClient from './apiClient'

export const orderService = {
  async createOrder(storeId, items) {
    const { data } = await apiClient.post(`/stores/${storeId}/orders`, {
      items: items.map(item => ({
        menu_id: item.menuId,
        quantity: item.quantity
      }))
    })
    return data
  },
  async getOrders(storeId, page = 1) {
    const { data } = await apiClient.get(`/stores/${storeId}/orders`, {
      params: { page }
    })
    return data
  }
}
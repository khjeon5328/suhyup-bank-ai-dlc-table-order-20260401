import apiClient from './apiClient'

export const orderService = {
  async createOrder(storeCode, items) {
    const { data } = await apiClient.post(`/stores/${storeCode}/orders/`, {
      items: items.map(item => ({
        menu_id: item.menuId,
        quantity: item.quantity
      }))
    })
    return data
  },
  async getOrders(storeCode, page = 1) {
    const { data } = await apiClient.get(`/stores/${storeCode}/orders/`, {
      params: { page }
    })
    return data
  }
}
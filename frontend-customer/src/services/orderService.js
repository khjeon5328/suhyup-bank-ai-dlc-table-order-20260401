import apiClient from './apiClient'

export const orderService = {
  async createOrder(storeId, tableId, sessionId, items) {
    const { data } = await apiClient.post(`/stores/${storeId}/orders`, {
      table_id: tableId,
      session_id: sessionId,
      items: items.map(item => ({
        menu_id: item.menuId,
        menu_name: item.name,
        quantity: item.quantity,
        unit_price: item.price
      }))
    })
    return data
  },
  async getOrders(storeId, sessionId, page = 1) {
    const { data } = await apiClient.get(`/stores/${storeId}/orders`, {
      params: { session_id: sessionId, page }
    })
    return data
  }
}
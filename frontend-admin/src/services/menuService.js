import apiClient from './apiClient'

export const menuService = {
  async getCategories(storeId) {
    const { data } = await apiClient.get(`/stores/${storeId}/menus/categories`)
    return data
  },
  async getMenus(storeId, categoryId = null) {
    const params = categoryId ? { category_id: categoryId } : {}
    const { data } = await apiClient.get(`/stores/${storeId}/menus`, { params })
    return data
  },
  async createMenu(storeId, menuData) {
    const { data } = await apiClient.post(`/stores/${storeId}/menus`, menuData)
    return data
  },
  async updateMenu(storeId, menuId, menuData) {
    const { data } = await apiClient.put(`/stores/${storeId}/menus/${menuId}`, menuData)
    return data
  },
  async deleteMenu(storeId, menuId) {
    await apiClient.delete(`/stores/${storeId}/menus/${menuId}`)
  },
  async updateMenuOrder(storeId, items) {
    await apiClient.put(`/stores/${storeId}/menus/order`, { items })
  }
}
import apiClient from './apiClient'

export const menuService = {
  async getCategories(storeCode) {
    const { data } = await apiClient.get(`/stores/${storeCode}/menus/categories`)
    return data
  },
  async getMenus(storeCode, categoryId = null) {
    const params = categoryId ? { category_id: categoryId } : {}
    const { data } = await apiClient.get(`/stores/${storeCode}/menus/`, { params })
    return data
  },
  async createMenu(storeCode, menuData) {
    const { data } = await apiClient.post(`/stores/${storeCode}/menus/`, menuData)
    return data
  },
  async updateMenu(storeCode, menuId, menuData) {
    const { data } = await apiClient.put(`/stores/${storeCode}/menus/${menuId}`, menuData)
    return data
  },
  async deleteMenu(storeCode, menuId) {
    await apiClient.delete(`/stores/${storeCode}/menus/${menuId}`)
  },
  async updateMenuOrder(storeCode, items) {
    await apiClient.put(`/stores/${storeCode}/menus/order`, { items })
  }
}
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
  async getMenu(storeId, menuId) {
    const { data } = await apiClient.get(`/stores/${storeId}/menus/${menuId}`)
    return data
  }
}
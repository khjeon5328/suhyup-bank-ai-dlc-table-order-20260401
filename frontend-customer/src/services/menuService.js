import apiClient from './apiClient'

export const menuService = {
  async getCategories(storeCode) {
    const { data } = await apiClient.get(`/stores/${storeCode}/menus/categories`)
    return data
  },
  async getMenus(storeCode, categoryId = null) {
    const params = categoryId ? { category_id: categoryId } : {}
    const { data } = await apiClient.get(`/stores/${storeCode}/menus`, { params })
    return data
  },
  async getMenu(storeCode, menuId) {
    const { data } = await apiClient.get(`/stores/${storeCode}/menus/${menuId}`)
    return data
  }
}
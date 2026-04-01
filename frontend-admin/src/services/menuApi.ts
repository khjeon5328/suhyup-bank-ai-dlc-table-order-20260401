import apiClient from './apiClient'
import type { ApiResponse } from '@/types/api'
import type {
  Menu,
  MenuCreateRequest,
  MenuUpdateRequest,
  MenuOrderUpdate,
  Category,
  CategoryCreateRequest,
  CategoryUpdateRequest,
  CategoryOrderUpdate,
} from '@/types/menu'

export const menuApi = {
  getMenus(storeId: number): Promise<ApiResponse<Menu[]>> {
    return apiClient.get(`/stores/${storeId}/menus`).then((res) => res.data)
  },

  createMenu(storeId: number, data: MenuCreateRequest): Promise<ApiResponse<Menu>> {
    return apiClient.post(`/stores/${storeId}/menus`, data).then((res) => res.data)
  },

  updateMenu(storeId: number, menuId: number, data: MenuUpdateRequest): Promise<ApiResponse<Menu>> {
    return apiClient.put(`/stores/${storeId}/menus/${menuId}`, data).then((res) => res.data)
  },

  deleteMenu(storeId: number, menuId: number): Promise<ApiResponse<null>> {
    return apiClient.delete(`/stores/${storeId}/menus/${menuId}`).then((res) => res.data)
  },

  updateMenuOrder(storeId: number, updates: MenuOrderUpdate[]): Promise<ApiResponse<null>> {
    return apiClient.put(`/stores/${storeId}/menus/order`, { updates }).then((res) => res.data)
  },

  getCategories(storeId: number): Promise<ApiResponse<Category[]>> {
    return apiClient.get(`/stores/${storeId}/menus/categories`).then((res) => res.data)
  },

  createCategory(storeId: number, data: CategoryCreateRequest): Promise<ApiResponse<Category>> {
    return apiClient.post(`/stores/${storeId}/menus/categories`, data).then((res) => res.data)
  },

  updateCategory(storeId: number, categoryId: number, data: CategoryUpdateRequest): Promise<ApiResponse<Category>> {
    return apiClient.put(`/stores/${storeId}/menus/categories/${categoryId}`, data).then((res) => res.data)
  },

  deleteCategory(storeId: number, categoryId: number): Promise<ApiResponse<null>> {
    return apiClient.delete(`/stores/${storeId}/menus/categories/${categoryId}`).then((res) => res.data)
  },

  updateCategoryOrder(storeId: number, updates: CategoryOrderUpdate[]): Promise<ApiResponse<null>> {
    return apiClient.put(`/stores/${storeId}/menus/categories/order`, { updates }).then((res) => res.data)
  },
}

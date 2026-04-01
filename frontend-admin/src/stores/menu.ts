import { ref } from 'vue'
import { defineStore } from 'pinia'
import { menuApi } from '@/services/menuApi'
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

export const useMenuStore = defineStore('menu', () => {
  const menus = ref<Menu[]>([])
  const categories = ref<Category[]>([])
  const selectedCategory = ref<string | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchMenus(storeId: number): Promise<void> {
    loading.value = true
    error.value = null
    try {
      const response = await menuApi.getMenus(storeId)
      menus.value = response.data
    } catch (e: unknown) {
      error.value = (e as Error).message
    } finally {
      loading.value = false
    }
  }

  async function createMenu(storeId: number, data: MenuCreateRequest): Promise<void> {
    const response = await menuApi.createMenu(storeId, data)
    menus.value.push(response.data)
  }

  async function updateMenu(storeId: number, menuId: number, data: MenuUpdateRequest): Promise<void> {
    const response = await menuApi.updateMenu(storeId, menuId, data)
    const index = menus.value.findIndex((m) => m.id === menuId)
    if (index !== -1) {
      menus.value[index] = response.data
    }
  }

  async function deleteMenu(storeId: number, menuId: number): Promise<void> {
    await menuApi.deleteMenu(storeId, menuId)
    menus.value = menus.value.filter((m) => m.id !== menuId)
  }

  async function updateMenuOrder(storeId: number, updates: MenuOrderUpdate[]): Promise<void> {
    await menuApi.updateMenuOrder(storeId, updates)
    updates.forEach(({ menuId, displayOrder }) => {
      const menu = menus.value.find((m) => m.id === menuId)
      if (menu) {
        menu.displayOrder = displayOrder
      }
    })
  }

  async function fetchCategories(storeId: number): Promise<void> {
    loading.value = true
    error.value = null
    try {
      const response = await menuApi.getCategories(storeId)
      categories.value = response.data
    } catch (e: unknown) {
      error.value = (e as Error).message
    } finally {
      loading.value = false
    }
  }

  async function createCategory(storeId: number, data: CategoryCreateRequest): Promise<void> {
    const response = await menuApi.createCategory(storeId, data)
    categories.value.push(response.data)
  }

  async function updateCategory(storeId: number, categoryId: number, data: CategoryUpdateRequest): Promise<void> {
    const response = await menuApi.updateCategory(storeId, categoryId, data)
    const index = categories.value.findIndex((c) => c.id === categoryId)
    if (index !== -1) {
      categories.value[index] = response.data
    }
  }

  async function deleteCategory(storeId: number, categoryId: number): Promise<void> {
    await menuApi.deleteCategory(storeId, categoryId)
    categories.value = categories.value.filter((c) => c.id !== categoryId)
  }

  async function updateCategoryOrder(storeId: number, updates: CategoryOrderUpdate[]): Promise<void> {
    await menuApi.updateCategoryOrder(storeId, updates)
    updates.forEach(({ categoryId, displayOrder }) => {
      const cat = categories.value.find((c) => c.id === categoryId)
      if (cat) {
        cat.displayOrder = displayOrder
      }
    })
  }

  function $reset(): void {
    menus.value = []
    categories.value = []
    selectedCategory.value = null
    loading.value = false
    error.value = null
  }

  return {
    menus,
    categories,
    selectedCategory,
    loading,
    error,
    fetchMenus,
    createMenu,
    updateMenu,
    deleteMenu,
    updateMenuOrder,
    fetchCategories,
    createCategory,
    updateCategory,
    deleteCategory,
    updateCategoryOrder,
    $reset,
  }
})

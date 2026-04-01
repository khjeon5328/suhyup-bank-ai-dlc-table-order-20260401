import { setActivePinia, createPinia } from 'pinia'
import { useMenuStore } from '@/stores/menu'

jest.mock('@/services/menuApi', () => ({
  menuApi: {
    getMenus: jest.fn(),
    createMenu: jest.fn(),
    updateMenu: jest.fn(),
    deleteMenu: jest.fn(),
    updateMenuOrder: jest.fn(),
    getCategories: jest.fn(),
    createCategory: jest.fn(),
    updateCategory: jest.fn(),
    deleteCategory: jest.fn(),
    updateCategoryOrder: jest.fn(),
  },
}))

describe('menu store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('should have correct initial state', () => {
    const store = useMenuStore()
    expect(store.menus).toEqual([])
    expect(store.categories).toEqual([])
    expect(store.loading).toBe(false)
    expect(store.error).toBeNull()
  })

  it('selectedCategory should be null initially', () => {
    const store = useMenuStore()
    expect(store.selectedCategory).toBeNull()
  })

  it('$reset should clear all state', () => {
    const store = useMenuStore()
    store.selectedCategory = 'test'
    store.loading = true
    store.$reset()
    expect(store.selectedCategory).toBeNull()
    expect(store.menus).toEqual([])
    expect(store.loading).toBe(false)
  })
})

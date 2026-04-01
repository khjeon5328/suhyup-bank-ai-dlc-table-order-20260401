import { defineStore } from 'pinia'

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: []
  }),
  getters: {
    totalAmount: (state) => state.items.reduce((sum, item) => sum + item.price * item.quantity, 0),
    totalItems: (state) => state.items.reduce((sum, item) => sum + item.quantity, 0),
    isEmpty: (state) => state.items.length === 0
  },
  actions: {
    addItem(menu) {
      const existing = this.items.find(item => item.menuId === menu.id)
      if (existing) {
        existing.quantity++
      } else {
        this.items.push({
          menuId: menu.id,
          name: menu.name,
          price: menu.price,
          quantity: 1,
          imageUrl: menu.image_url || null
        })
      }
    },
    removeItem(menuId) {
      this.items = this.items.filter(item => item.menuId !== menuId)
    },
    increaseQuantity(menuId) {
      const item = this.items.find(item => item.menuId === menuId)
      if (item) item.quantity++
    },
    decreaseQuantity(menuId) {
      const item = this.items.find(item => item.menuId === menuId)
      if (!item) return
      if (item.quantity <= 1) {
        this.removeItem(menuId)
      } else {
        item.quantity--
      }
    },
    clearCart() {
      this.items = []
    }
  },
  persist: {
    key: 'cart',
    storage: localStorage,
    pick: ['items']
  }
})
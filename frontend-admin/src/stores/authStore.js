import { defineStore } from 'pinia'
import { authService } from '../services/authService'

export const useAuthStore = defineStore('adminAuth', {
  state: () => ({ token: null, storeId: null, userId: null, username: null, role: null }),
  getters: {
    isAuthenticated: (s) => !!s.token,
    isOwner: (s) => s.role === 'owner'
  },
  actions: {
    async login(storeCode, username, password) {
      const data = await authService.login(storeCode, username, password)
      this.token = data.access_token
      this.storeId = data.user.store_id
      this.userId = data.user.id
      this.username = data.user.username
      this.role = data.user.role
      localStorage.setItem('admin_token', data.access_token)
      return data
    },
    logout() {
      this.token = null; this.storeId = null; this.userId = null; this.username = null; this.role = null
      localStorage.removeItem('admin_token')
    }
  },
  persist: { key: 'adminAuth', storage: localStorage, pick: ['token', 'storeId', 'userId', 'username', 'role'] }
})
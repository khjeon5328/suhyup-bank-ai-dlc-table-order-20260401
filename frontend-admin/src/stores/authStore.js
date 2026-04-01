import { defineStore } from 'pinia'
import { authService } from '@/services/authService'

export const useAuthStore = defineStore('adminAuth', {
  state: () => ({ token: null, storeCode: null, userId: null, username: null, role: null }),
  getters: {
    isAuthenticated: (s) => !!s.token,
    isOwner: (s) => s.role === 'owner'
  },
  actions: {
    async login(storeCode, username, password) {
      const data = await authService.login(storeCode, username, password)
      this.token = data.access_token
      this.storeCode = data.user.store_code
      this.userId = data.user.id
      this.username = data.user.username
      this.role = data.user.role
      localStorage.setItem('admin_token', data.access_token)
      return data
    },
    logout() {
      this.token = null; this.storeCode = null; this.userId = null; this.username = null; this.role = null
      localStorage.removeItem('admin_token')
    }
  },
  persist: { key: 'adminAuth', storage: localStorage, pick: ['token', 'storeCode', 'userId', 'username', 'role'] }
})
import { defineStore } from 'pinia'
import { authService } from '../services/authService'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: null,
    storeId: null,
    tableId: null,
    sessionId: null,
    storeCode: null,
    tableNo: null
  }),
  getters: {
    isAuthenticated: (state) => !!state.token
  },
  actions: {
    async login(storeCode, tableNo, password) {
      const data = await authService.loginTable(storeCode, tableNo, password)
      this.token = data.access_token
      this.storeId = data.table.store_id
      this.tableId = data.table.id
      this.sessionId = data.table.session_id
      this.storeCode = storeCode
      this.tableNo = tableNo
      localStorage.setItem('token', data.access_token)
      return data
    },
    logout() {
      this.token = null
      this.storeId = null
      this.tableId = null
      this.sessionId = null
      localStorage.removeItem('token')
    },
    updateSessionId(sessionId) {
      this.sessionId = sessionId
    }
  },
  persist: {
    key: 'auth',
    storage: localStorage,
    pick: ['token', 'storeId', 'tableId', 'sessionId', 'storeCode', 'tableNo']
  }
})
import { defineStore } from 'pinia'
import { authService } from '../services/authService'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: null,
    storeCode: null,
    tableNo: null,
    sessionId: null
  }),
  getters: {
    isAuthenticated: (state) => !!state.token
  },
  actions: {
    async login(storeCode, tableNo, password) {
      const data = await authService.loginTable(storeCode, tableNo, password)
      this.token = data.access_token
      this.storeCode = data.table.store_code
      this.tableNo = data.table.table_no
      this.sessionId = data.table.session_id
      localStorage.setItem('token', data.access_token)
      return data
    },
    logout() {
      this.token = null
      this.storeCode = null
      this.tableNo = null
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
    pick: ['token', 'storeCode', 'tableNo', 'sessionId']
  }
})
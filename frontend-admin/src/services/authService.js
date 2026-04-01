import apiClient from './apiClient'

export const authService = {
  async login(storeCode, username, password) {
    const { data } = await apiClient.post('/auth/login/admin', { store_code: storeCode, username, password })
    return data
  }
}
import apiClient from './apiClient'

export const userService = {
  async getUsers(storeCode) {
    const { data } = await apiClient.get(`/stores/${storeCode}/users`)
    return data
  },
  async createUser(storeCode, userData) {
    const { data } = await apiClient.post(`/stores/${storeCode}/users`, userData)
    return data
  },
  async updateUser(storeCode, userId, userData) {
    const { data } = await apiClient.put(`/stores/${storeCode}/users/${userId}`, userData)
    return data
  },
  async deleteUser(storeCode, userId) {
    await apiClient.delete(`/stores/${storeCode}/users/${userId}`)
  }
}
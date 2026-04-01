import apiClient from './apiClient'

export const userService = {
  async getUsers(storeId) {
    const { data } = await apiClient.get(`/stores/${storeId}/users`)
    return data
  },
  async createUser(storeId, userData) {
    const { data } = await apiClient.post(`/stores/${storeId}/users`, userData)
    return data
  },
  async updateUser(storeId, userId, userData) {
    const { data } = await apiClient.put(`/stores/${storeId}/users/${userId}`, userData)
    return data
  },
  async deleteUser(storeId, userId) {
    await apiClient.delete(`/stores/${storeId}/users/${userId}`)
  }
}
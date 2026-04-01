import apiClient from './apiClient'
import type { ApiResponse } from '@/types/api'
import type { User, UserCreateRequest, UserUpdateRequest } from '@/types/user'

export const userApi = {
  getUsers(storeId: number): Promise<ApiResponse<User[]>> {
    return apiClient.get(`/stores/${storeId}/users`).then((res) => res.data)
  },

  createUser(storeId: number, data: UserCreateRequest): Promise<ApiResponse<User>> {
    return apiClient.post(`/stores/${storeId}/users`, data).then((res) => res.data)
  },

  updateUser(storeId: number, userId: number, data: UserUpdateRequest): Promise<ApiResponse<User>> {
    return apiClient.patch(`/stores/${storeId}/users/${userId}`, data).then((res) => res.data)
  },

  deleteUser(storeId: number, userId: number): Promise<ApiResponse<null>> {
    return apiClient.delete(`/stores/${storeId}/users/${userId}`).then((res) => res.data)
  },
}

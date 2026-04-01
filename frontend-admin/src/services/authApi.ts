import apiClient from './apiClient'
import type { ApiResponse } from '@/types/api'
import type { LoginCredentials, AuthTokens } from '@/types/auth'

export const authApi = {
  login(credentials: LoginCredentials): Promise<ApiResponse<AuthTokens>> {
    return apiClient.post('/auth/login/admin', credentials).then((res) => res.data)
  },

  refresh(): Promise<ApiResponse<AuthTokens>> {
    return apiClient.post('/auth/refresh').then((res) => res.data)
  },

  logout(): Promise<ApiResponse<null>> {
    return apiClient.post('/auth/logout').then((res) => res.data)
  },
}

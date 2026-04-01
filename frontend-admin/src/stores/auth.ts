import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { authApi } from '@/services/authApi'
import { sseService } from '@/services/sseService'
import type { LoginCredentials, AuthUser, AuthTokens } from '@/types/auth'
import { UserRole } from '@/types/auth'

function decodeJwtPayload(token: string): Record<string, unknown> {
  try {
    const base64Url = token.split('.')[1]
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join(''),
    )
    return JSON.parse(jsonPayload)
  } catch {
    return {}
  }
}

function extractUser(token: string): AuthUser | null {
  const payload = decodeJwtPayload(token)
  if (!payload.sub) return null
  return {
    id: payload.sub as number,
    storeId: payload.storeId as number,
    username: payload.username as string,
    role: payload.role as UserRole,
    storeName: (payload.storeName as string) || '',
  }
}

export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref<string | null>(null)
  const user = ref<AuthUser | null>(null)

  const isAuthenticated = computed(() => !!accessToken.value && !!user.value)
  const isOwner = computed(() => user.value?.role === UserRole.OWNER)
  const isManager = computed(() => user.value?.role === UserRole.MANAGER)
  const storeId = computed(() => user.value?.storeId ?? null)

  function setTokens(tokens: AuthTokens): void {
    accessToken.value = tokens.accessToken
    user.value = extractUser(tokens.accessToken)
  }

  async function login(credentials: LoginCredentials): Promise<void> {
    const response = await authApi.login(credentials)
    setTokens(response.data)
    if (user.value?.storeId) {
      sseService.connect(user.value.storeId)
    }
  }

  async function refreshToken(): Promise<string> {
    const response = await authApi.refresh()
    setTokens(response.data)
    return response.data.accessToken
  }

  async function logout(): Promise<void> {
    try {
      await authApi.logout()
    } catch {
      // ignore logout errors
    } finally {
      sseService.disconnect()
      $reset()
    }
  }

  async function initAuth(): Promise<boolean> {
    try {
      const response = await authApi.refresh()
      setTokens(response.data)
      if (user.value?.storeId) {
        sseService.connect(user.value.storeId)
      }
      return true
    } catch {
      $reset()
      return false
    }
  }

  function $reset(): void {
    accessToken.value = null
    user.value = null
  }

  return {
    accessToken,
    user,
    isAuthenticated,
    isOwner,
    isManager,
    storeId,
    login,
    refreshToken,
    logout,
    initAuth,
    $reset,
  }
})

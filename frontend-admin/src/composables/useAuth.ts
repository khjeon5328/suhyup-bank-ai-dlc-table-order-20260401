import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import type { LoginCredentials } from '@/types/auth'

export function useAuth() {
  const authStore = useAuthStore()

  const user = computed(() => authStore.user)
  const isAuthenticated = computed(() => authStore.isAuthenticated)
  const isOwner = computed(() => authStore.isOwner)
  const isManager = computed(() => authStore.isManager)

  async function login(credentials: LoginCredentials): Promise<void> {
    await authStore.login(credentials)
  }

  async function logout(): Promise<void> {
    await authStore.logout()
  }

  return { user, isAuthenticated, isOwner, isManager, login, logout }
}

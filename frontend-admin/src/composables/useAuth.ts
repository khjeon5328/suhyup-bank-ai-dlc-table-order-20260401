import { computed } from 'vue'
import { useAuthStore } from '@/stores/authStore'

export function useAuth() {
  const authStore = useAuthStore()

  const isAuthenticated = computed(() => authStore.isAuthenticated)
  const isOwner = computed(() => authStore.isOwner)

  async function login(credentials: { storeId: string; username: string; password: string }): Promise<void> {
    await authStore.login(credentials.storeId, credentials.username, credentials.password)
  }

  function logout(): void {
    authStore.logout()
  }

  return { isAuthenticated, isOwner, login, logout }
}

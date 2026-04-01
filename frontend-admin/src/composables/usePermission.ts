import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

export function usePermission() {
  const authStore = useAuthStore()

  const canDeleteOrder = computed(() => authStore.isOwner)
  const canManageMenu = computed(() => authStore.isOwner)
  const canManageUser = computed(() => authStore.isOwner)
  const canSetupTable = computed(() => authStore.isOwner)

  return { canDeleteOrder, canManageMenu, canManageUser, canSetupTable }
}

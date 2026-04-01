import { setActivePinia, createPinia } from 'pinia'
import { usePermission } from '@/composables/usePermission'
import { useAuthStore } from '@/stores/auth'
import { UserRole } from '@/types/auth'

jest.mock('@/services/authApi', () => ({
  authApi: { login: jest.fn(), refresh: jest.fn(), logout: jest.fn() },
}))
jest.mock('@/services/sseService', () => ({
  sseService: { connect: jest.fn(), disconnect: jest.fn() },
}))

describe('usePermission', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('should deny all permissions when unauthenticated', () => {
    const { canDeleteOrder, canManageMenu, canManageUser, canSetupTable } = usePermission()
    expect(canDeleteOrder.value).toBe(false)
    expect(canManageMenu.value).toBe(false)
    expect(canManageUser.value).toBe(false)
    expect(canSetupTable.value).toBe(false)
  })

  it('should grant all permissions for owner', () => {
    const authStore = useAuthStore()
    authStore.user = { id: 1, storeId: 1, username: 'admin', role: UserRole.OWNER, storeName: 'Test' }
    authStore.accessToken = 'token'

    const { canDeleteOrder, canManageMenu, canManageUser, canSetupTable } = usePermission()
    expect(canDeleteOrder.value).toBe(true)
    expect(canManageMenu.value).toBe(true)
    expect(canManageUser.value).toBe(true)
    expect(canSetupTable.value).toBe(true)
  })

  it('should deny permissions for manager', () => {
    const authStore = useAuthStore()
    authStore.user = { id: 2, storeId: 1, username: 'mgr', role: UserRole.MANAGER, storeName: 'Test' }
    authStore.accessToken = 'token'

    const { canDeleteOrder, canManageMenu, canManageUser, canSetupTable } = usePermission()
    expect(canDeleteOrder.value).toBe(false)
    expect(canManageMenu.value).toBe(false)
    expect(canManageUser.value).toBe(false)
    expect(canSetupTable.value).toBe(false)
  })
})

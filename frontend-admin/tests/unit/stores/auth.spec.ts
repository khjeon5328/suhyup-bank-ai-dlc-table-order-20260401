import { setActivePinia, createPinia } from 'pinia'
import { useAuthStore } from '@/stores/auth'

jest.mock('@/services/authApi', () => ({
  authApi: {
    login: jest.fn(),
    refresh: jest.fn(),
    logout: jest.fn(),
  },
}))

jest.mock('@/services/sseService', () => ({
  sseService: {
    connect: jest.fn(),
    disconnect: jest.fn(),
  },
}))

describe('auth store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('should have correct initial state', () => {
    const store = useAuthStore()
    expect(store.accessToken).toBeNull()
    expect(store.user).toBeNull()
  })

  it('should reset state with $reset', () => {
    const store = useAuthStore()
    store.accessToken = 'some-token'
    store.$reset()
    expect(store.accessToken).toBeNull()
    expect(store.user).toBeNull()
  })

  it('isOwner should be false when unauthenticated', () => {
    const store = useAuthStore()
    expect(store.isOwner).toBe(false)
  })

  it('isManager should be false when unauthenticated', () => {
    const store = useAuthStore()
    expect(store.isManager).toBe(false)
  })

  it('isAuthenticated should be false when no token', () => {
    const store = useAuthStore()
    expect(store.isAuthenticated).toBe(false)
  })
})

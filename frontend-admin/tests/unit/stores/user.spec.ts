import { setActivePinia, createPinia } from 'pinia'
import { useUserStore } from '@/stores/user'

jest.mock('@/services/userApi', () => ({
  userApi: {
    getUsers: jest.fn(),
    createUser: jest.fn(),
    updateUser: jest.fn(),
    deleteUser: jest.fn(),
  },
}))

describe('user store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('should have correct initial state', () => {
    const store = useUserStore()
    expect(store.users).toEqual([])
    expect(store.loading).toBe(false)
    expect(store.error).toBeNull()
  })

  it('$reset should clear all state', () => {
    const store = useUserStore()
    store.loading = true
    store.error = 'some error'
    store.$reset()
    expect(store.users).toEqual([])
    expect(store.loading).toBe(false)
    expect(store.error).toBeNull()
  })
})

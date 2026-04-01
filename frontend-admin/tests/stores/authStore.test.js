import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useAuthStore } from '../../src/stores/authStore'

describe('admin authStore', () => {
  let store
  beforeEach(() => { setActivePinia(createPinia()); store = useAuthStore(); localStorage.clear() })

  it('초기 상태는 미인증', () => {
    expect(store.isAuthenticated).toBe(false)
    expect(store.isOwner).toBe(false)
  })

  it('logout 시 상태 초기화', () => {
    store.token = 'test'; store.role = 'owner'; store.storeCode = 'STORE001'
    store.logout()
    expect(store.token).toBeNull()
    expect(store.role).toBeNull()
    expect(store.isAuthenticated).toBe(false)
  })

  it('owner 역할 판별', () => {
    store.role = 'owner'
    expect(store.isOwner).toBe(true)
    store.role = 'manager'
    expect(store.isOwner).toBe(false)
  })
})
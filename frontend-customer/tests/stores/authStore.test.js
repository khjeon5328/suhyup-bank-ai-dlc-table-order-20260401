import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useAuthStore } from '../../src/stores/authStore'

describe('authStore', () => {
  let store

  beforeEach(() => {
    setActivePinia(createPinia())
    store = useAuthStore()
    localStorage.clear()
  })

  it('초기 상태는 미인증', () => {
    expect(store.isAuthenticated).toBe(false)
    expect(store.token).toBeNull()
  })

  it('logout 시 토큰 제거', () => {
    store.token = 'test-token'
    store.storeId = 1
    store.logout()
    expect(store.token).toBeNull()
    expect(store.storeId).toBeNull()
    expect(localStorage.getItem('token')).toBeNull()
  })

  it('sessionId 업데이트', () => {
    store.updateSessionId(42)
    expect(store.sessionId).toBe(42)
  })
})
jest.mock('@/stores/auth', () => ({
  useAuthStore: jest.fn(() => ({ accessToken: null })),
}))
jest.mock('@/router', () => ({ push: jest.fn() }))

import apiClient from '@/services/apiClient'

describe('apiClient', () => {
  it('should have correct baseURL from env', () => {
    expect(apiClient.defaults.baseURL).toBeDefined()
  })

  it('should have withCredentials set to true', () => {
    expect(apiClient.defaults.withCredentials).toBe(true)
  })

  it('should have timeout of 10000', () => {
    expect(apiClient.defaults.timeout).toBe(10000)
  })

  it('should have Content-Type header support', () => {
    expect(apiClient.defaults.headers).toBeDefined()
  })
})

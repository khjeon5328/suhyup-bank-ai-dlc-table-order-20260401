import { authApi } from '@/services/authApi'
import apiClient from '@/services/apiClient'

jest.mock('@/services/apiClient', () => ({
  __esModule: true,
  default: {
    post: jest.fn(),
  },
}))

const mockPost = apiClient.post as jest.Mock

describe('authApi', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('login should POST to /auth/login/admin', async () => {
    const mockResponse = { data: { success: true, data: { accessToken: 'token' } } }
    mockPost.mockResolvedValue(mockResponse)

    const credentials = { storeId: '1', username: 'admin', password: 'pass' }
    await authApi.login(credentials)

    expect(mockPost).toHaveBeenCalledWith('/auth/login/admin', credentials)
  })

  it('refresh should POST to /auth/refresh', async () => {
    const mockResponse = { data: { success: true, data: { accessToken: 'newToken' } } }
    mockPost.mockResolvedValue(mockResponse)

    await authApi.refresh()

    expect(mockPost).toHaveBeenCalledWith('/auth/refresh')
  })

  it('logout should POST to /auth/logout', async () => {
    const mockResponse = { data: { success: true, data: null } }
    mockPost.mockResolvedValue(mockResponse)

    await authApi.logout()

    expect(mockPost).toHaveBeenCalledWith('/auth/logout')
  })
})

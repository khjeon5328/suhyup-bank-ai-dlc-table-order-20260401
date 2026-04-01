import { orderApi } from '@/services/orderApi'
import apiClient from '@/services/apiClient'
import { OrderStatus } from '@/types/order'

jest.mock('@/services/apiClient', () => ({
  __esModule: true,
  default: {
    get: jest.fn(),
    patch: jest.fn(),
    delete: jest.fn(),
  },
}))

const mockGet = apiClient.get as jest.Mock
const mockPatch = apiClient.patch as jest.Mock
const mockDelete = apiClient.delete as jest.Mock

describe('orderApi', () => {
  beforeEach(() => jest.clearAllMocks())

  it('getOrders without tableId', async () => {
    mockGet.mockResolvedValue({ data: { data: [] } })
    await orderApi.getOrders(1)
    expect(mockGet).toHaveBeenCalledWith('/stores/1/orders', { params: {} })
  })

  it('getOrders with tableId', async () => {
    mockGet.mockResolvedValue({ data: { data: [] } })
    await orderApi.getOrders(1, 5)
    expect(mockGet).toHaveBeenCalledWith('/stores/1/orders', { params: { tableId: 5 } })
  })

  it('updateStatus should PATCH', async () => {
    mockPatch.mockResolvedValue({ data: { data: {} } })
    await orderApi.updateStatus(1, 10, OrderStatus.PREPARING)
    expect(mockPatch).toHaveBeenCalledWith('/stores/1/orders/10/status', { status: OrderStatus.PREPARING })
  })

  it('deleteOrder should DELETE', async () => {
    mockDelete.mockResolvedValue({ data: { data: null } })
    await orderApi.deleteOrder(1, 10)
    expect(mockDelete).toHaveBeenCalledWith('/stores/1/orders/10')
  })

  it('getHistory should GET with date params', async () => {
    mockGet.mockResolvedValue({ data: { data: [] } })
    await orderApi.getHistory(1, 2, '2024-01-01', '2024-01-31')
    expect(mockGet).toHaveBeenCalledWith('/stores/1/tables/2/history', {
      params: { dateFrom: '2024-01-01', dateTo: '2024-01-31' },
    })
  })
})

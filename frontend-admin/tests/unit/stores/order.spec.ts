import { setActivePinia, createPinia } from 'pinia'
import { useOrderStore } from '@/stores/order'
import { SSEEventType } from '@/types/sse'
import { OrderStatus } from '@/types/order'
import type { SSEEvent, SSEOrderCreatedData, SSEOrderStatusChangedData, SSEOrderDeletedData } from '@/types/sse'
import type { Order } from '@/types/order'

jest.mock('@/services/orderApi', () => ({
  orderApi: {
    getOrders: jest.fn(),
    updateStatus: jest.fn(),
    deleteOrder: jest.fn(),
    getHistory: jest.fn(),
  },
}))

const createOrder = (overrides: Partial<Order> = {}): Order => ({
  id: 1,
  orderNumber: 'ORD-001',
  storeId: 1,
  tableId: 1,
  sessionId: 1,
  items: [],
  totalAmount: 10000,
  status: OrderStatus.PENDING,
  createdAt: '2024-01-01',
  updatedAt: '2024-01-01',
  ...overrides,
})

describe('order store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('should have correct initial state', () => {
    const store = useOrderStore()
    expect(store.ordersByTable.size).toBe(0)
    expect(store.orderHistory).toEqual([])
    expect(store.loading).toBe(false)
    expect(store.error).toBeNull()
  })

  it('handleSSEEvent ORDER_CREATED should add order', () => {
    const store = useOrderStore()
    const order = createOrder({ id: 1, tableId: 5 })
    const event: SSEEvent = {
      type: SSEEventType.ORDER_CREATED,
      data: { order } as SSEOrderCreatedData,
      timestamp: new Date().toISOString(),
    }
    store.handleSSEEvent(event)
    expect(store.ordersByTable.get(5)).toHaveLength(1)
  })

  it('handleSSEEvent ORDER_STATUS_CHANGED should update status', () => {
    const store = useOrderStore()
    const order = createOrder({ id: 1, tableId: 5 })
    store.ordersByTable.set(5, [order])

    const event: SSEEvent = {
      type: SSEEventType.ORDER_STATUS_CHANGED,
      data: { orderId: 1, status: OrderStatus.PREPARING, tableId: 5 } as SSEOrderStatusChangedData,
      timestamp: new Date().toISOString(),
    }
    store.handleSSEEvent(event)
    expect(store.ordersByTable.get(5)![0].status).toBe(OrderStatus.PREPARING)
  })

  it('handleSSEEvent ORDER_DELETED should remove order', () => {
    const store = useOrderStore()
    const order = createOrder({ id: 1, tableId: 5 })
    store.ordersByTable.set(5, [order])

    const event: SSEEvent = {
      type: SSEEventType.ORDER_DELETED,
      data: { orderId: 1, tableId: 5 } as SSEOrderDeletedData,
      timestamp: new Date().toISOString(),
    }
    store.handleSSEEvent(event)
    expect(store.ordersByTable.get(5)).toHaveLength(0)
  })

  it('$reset should clear all state', () => {
    const store = useOrderStore()
    store.ordersByTable.set(1, [createOrder()])
    store.loading = true
    store.$reset()
    expect(store.ordersByTable.size).toBe(0)
    expect(store.loading).toBe(false)
  })
})

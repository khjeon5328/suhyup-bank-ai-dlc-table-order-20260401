import { setActivePinia, createPinia } from 'pinia'
import { useTableStore } from '@/stores/table'

jest.mock('@/services/tableApi', () => ({
  tableApi: {
    getTables: jest.fn(),
    setupTable: jest.fn(),
    endSession: jest.fn(),
  },
}))

describe('table store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('should have correct initial state', () => {
    const store = useTableStore()
    expect(store.tables).toEqual([])
    expect(store.newOrderTableIds.size).toBe(0)
    expect(store.loading).toBe(false)
    expect(store.error).toBeNull()
  })

  it('addNewOrderAlert should add tableId to set', () => {
    const store = useTableStore()
    store.addNewOrderAlert(5)
    expect(store.newOrderTableIds.has(5)).toBe(true)
  })

  it('markAsRead should remove tableId from set', () => {
    const store = useTableStore()
    store.addNewOrderAlert(5)
    store.markAsRead(5)
    expect(store.newOrderTableIds.has(5)).toBe(false)
  })

  it('$reset should clear all state', () => {
    const store = useTableStore()
    store.addNewOrderAlert(1)
    store.loading = true
    store.$reset()
    expect(store.newOrderTableIds.size).toBe(0)
    expect(store.loading).toBe(false)
  })
})

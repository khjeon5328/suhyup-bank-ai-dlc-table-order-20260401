import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useOrderStore } from '../../src/stores/orderStore'

describe('admin orderStore', () => {
  let store
  beforeEach(() => { setActivePinia(createPinia()); store = useOrderStore() })

  it('초기 상태', () => {
    expect(store.orders).toEqual([])
    expect(store.isLoading).toBe(false)
    expect(store.sseConnected).toBe(false)
  })

  it('addOrder로 주문 추가', () => {
    store.addOrder({ id: 1, table_id: 1, total_amount: 9000, status: 'pending' })
    expect(store.orders).toHaveLength(1)
  })

  it('updateOrderInList로 상태 변경', () => {
    store.addOrder({ id: 1, table_id: 1, total_amount: 9000, status: 'pending' })
    store.updateOrderInList(1, 'preparing')
    expect(store.orders[0].status).toBe('preparing')
  })

  it('removeOrderFromList로 주문 삭제', () => {
    store.addOrder({ id: 1, table_id: 1, total_amount: 9000, status: 'pending' })
    store.addOrder({ id: 2, table_id: 1, total_amount: 8000, status: 'pending' })
    store.removeOrderFromList(1)
    expect(store.orders).toHaveLength(1)
    expect(store.orders[0].id).toBe(2)
  })

  it('ordersByTable 그룹핑', () => {
    store.addOrder({ id: 1, table_id: 1, total_amount: 9000, status: 'pending' })
    store.addOrder({ id: 2, table_id: 1, total_amount: 8000, status: 'pending' })
    store.addOrder({ id: 3, table_id: 2, total_amount: 5000, status: 'pending' })
    const groups = store.ordersByTable
    expect(groups).toHaveLength(2)
    const t1 = groups.find(g => g.tableId === 1)
    expect(t1.orders).toHaveLength(2)
    expect(t1.totalAmount).toBe(17000)
  })
})
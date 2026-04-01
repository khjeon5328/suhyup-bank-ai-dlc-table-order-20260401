import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useCartStore } from '../../src/stores/cartStore'

const mockMenu = { id: 1, name: '김치찌개', price: 9000, image_url: null }
const mockMenu2 = { id: 2, name: '된장찌개', price: 8000, image_url: null }

describe('cartStore', () => {
  let store

  beforeEach(() => {
    setActivePinia(createPinia())
    store = useCartStore()
  })

  it('초기 상태는 빈 장바구니', () => {
    expect(store.items).toEqual([])
    expect(store.isEmpty).toBe(true)
    expect(store.totalAmount).toBe(0)
    expect(store.totalItems).toBe(0)
  })

  it('메뉴 추가 시 장바구니에 항목 생성', () => {
    store.addItem(mockMenu)
    expect(store.items).toHaveLength(1)
    expect(store.items[0].menuId).toBe(1)
    expect(store.items[0].quantity).toBe(1)
    expect(store.totalAmount).toBe(9000)
  })

  it('같은 메뉴 재추가 시 수량 증가', () => {
    store.addItem(mockMenu)
    store.addItem(mockMenu)
    expect(store.items).toHaveLength(1)
    expect(store.items[0].quantity).toBe(2)
    expect(store.totalAmount).toBe(18000)
  })

  it('수량 증가', () => {
    store.addItem(mockMenu)
    store.increaseQuantity(1)
    expect(store.items[0].quantity).toBe(2)
  })

  it('수량 감소', () => {
    store.addItem(mockMenu)
    store.addItem(mockMenu)
    store.decreaseQuantity(1)
    expect(store.items[0].quantity).toBe(1)
  })

  it('수량 1에서 감소 시 항목 삭제', () => {
    store.addItem(mockMenu)
    store.decreaseQuantity(1)
    expect(store.items).toHaveLength(0)
  })

  it('항목 삭제', () => {
    store.addItem(mockMenu)
    store.addItem(mockMenu2)
    store.removeItem(1)
    expect(store.items).toHaveLength(1)
    expect(store.items[0].menuId).toBe(2)
  })

  it('전체 비우기', () => {
    store.addItem(mockMenu)
    store.addItem(mockMenu2)
    store.clearCart()
    expect(store.items).toHaveLength(0)
    expect(store.isEmpty).toBe(true)
  })

  it('총 금액 계산', () => {
    store.addItem(mockMenu)
    store.addItem(mockMenu2)
    store.addItem(mockMenu)
    expect(store.totalAmount).toBe(9000 * 2 + 8000)
    expect(store.totalItems).toBe(3)
  })
})
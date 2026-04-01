import { describe, it, expect } from 'vitest'
import { formatPrice, formatDateTime, formatOrderNo } from '../../src/utils/formatters'

describe('formatPrice', () => {
  it('가격을 한국 원화 형식으로 포맷', () => {
    expect(formatPrice(9000)).toBe('9,000원')
    expect(formatPrice(12500)).toBe('12,500원')
    expect(formatPrice(0)).toBe('0원')
  })
})

describe('formatDateTime', () => {
  it('날짜를 MM/DD HH:mm 형식으로 포맷', () => {
    const result = formatDateTime('2026-04-01T14:30:00')
    expect(result).toBe('04/01 14:30')
  })
})

describe('formatOrderNo', () => {
  it('주문 번호 반환', () => {
    expect(formatOrderNo('ORD-20260401-001')).toBe('ORD-20260401-001')
  })
  it('null이면 - 반환', () => {
    expect(formatOrderNo(null)).toBe('-')
  })
})
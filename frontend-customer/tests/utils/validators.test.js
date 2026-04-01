import { describe, it, expect } from 'vitest'
import { validateStoreCode, validateTableNo, validatePassword } from '../../src/utils/validators'

describe('validateStoreCode', () => {
  it('빈 값이면 에러', () => {
    expect(validateStoreCode('')).toBeTruthy()
    expect(validateStoreCode(null)).toBeTruthy()
  })
  it('정상 값이면 null', () => {
    expect(validateStoreCode('STORE001')).toBeNull()
  })
  it('50자 초과 시 에러', () => {
    expect(validateStoreCode('a'.repeat(51))).toBeTruthy()
  })
})

describe('validateTableNo', () => {
  it('빈 값이면 에러', () => {
    expect(validateTableNo('')).toBeTruthy()
  })
  it('양의 정수면 null', () => {
    expect(validateTableNo('1')).toBeNull()
    expect(validateTableNo('5')).toBeNull()
  })
  it('0이나 음수면 에러', () => {
    expect(validateTableNo('0')).toBeTruthy()
    expect(validateTableNo('-1')).toBeTruthy()
  })
})

describe('validatePassword', () => {
  it('빈 값이면 에러', () => {
    expect(validatePassword('')).toBeTruthy()
  })
  it('정상 값이면 null', () => {
    expect(validatePassword('1234')).toBeNull()
  })
})
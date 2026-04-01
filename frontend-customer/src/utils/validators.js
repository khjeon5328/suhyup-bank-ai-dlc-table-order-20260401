export function validateStoreCode(value) {
  if (!value || typeof value !== 'string') return '매장 코드를 입력해 주세요'
  if (value.length > 50) return '매장 코드는 50자 이내여야 합니다'
  return null
}

export function validateTableNo(value) {
  const num = Number(value)
  if (!value || isNaN(num) || num < 1 || !Number.isInteger(num)) return '올바른 테이블 번호를 입력해 주세요'
  return null
}

export function validatePassword(value) {
  if (!value || typeof value !== 'string' || value.length < 1) return '비밀번호를 입력해 주세요'
  return null
}
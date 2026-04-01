export function formatPrice(amount) {
  return `${Number(amount).toLocaleString('ko-KR')}원`
}

export function formatDateTime(dateStr) {
  const d = new Date(dateStr)
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  const hours = String(d.getHours()).padStart(2, '0')
  const minutes = String(d.getMinutes()).padStart(2, '0')
  return `${month}/${day} ${hours}:${minutes}`
}

export function formatOrderNo(orderNo) {
  return orderNo || '-'
}
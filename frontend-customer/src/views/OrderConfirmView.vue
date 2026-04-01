<template>
  <div class="confirm-page">
    <h1 class="page-title">주문 확인</h1>
    <div class="order-items" data-testid="confirm-items">
      <div v-for="item in cartStore.items" :key="item.menuId" class="confirm-item">
        <span class="item-name">{{ item.name }}</span>
        <span class="item-qty">x{{ item.quantity }}</span>
        <span class="item-subtotal">{{ formatPrice(item.price * item.quantity) }}</span>
      </div>
    </div>
    <div class="total-row" data-testid="confirm-total">
      <span>총 금액</span>
      <span class="total-amount">{{ formatPrice(cartStore.totalAmount) }}</span>
    </div>
    <p v-if="errorMsg" class="error" data-testid="confirm-error">{{ errorMsg }}</p>
    <button class="confirm-btn" :disabled="orderStore.isLoading || cartStore.isEmpty"
            @click="handleOrder" data-testid="confirm-submit">
      {{ orderStore.isLoading ? '주문 중...' : '주문 확정' }}
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '../stores/cartStore'
import { useOrderStore } from '../stores/orderStore'
import { formatPrice } from '../utils/formatters'

const router = useRouter()
const cartStore = useCartStore()
const orderStore = useOrderStore()
const errorMsg = ref('')

// 빈 장바구니로 직접 접근 시 메뉴 화면으로 리다이렉트
if (cartStore.isEmpty) {
  router.push('/')
}

async function handleOrder() {
  errorMsg.value = ''
  try {
    const data = await orderStore.createOrder()
    router.push({ name: 'OrderResult', params: { orderId: data.id } })
  } catch (err) {
    errorMsg.value = err.response?.data?.detail || '주문에 실패했습니다. 다시 시도해 주세요.'
  }
}
</script>

<style scoped>
.confirm-page { padding: 16px; }
.page-title { font-size: 20px; margin-bottom: 16px; }
.order-items { background: #fff; border-radius: 12px; padding: 16px; margin-bottom: 16px; }
.confirm-item { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #f0f0f0; }
.confirm-item:last-child { border-bottom: none; }
.item-name { flex: 1; }
.item-qty { width: 50px; text-align: center; color: #666; }
.item-subtotal { width: 90px; text-align: right; font-weight: 600; }
.total-row { display: flex; justify-content: space-between; background: #fff; border-radius: 12px; padding: 16px; margin-bottom: 16px; font-size: 18px; }
.total-amount { font-weight: 700; color: #1976d2; font-size: 22px; }
.error { color: #f44336; text-align: center; margin-bottom: 12px; }
.confirm-btn { width: 100%; padding: 16px; background: #f44336; color: #fff; border: none; border-radius: 8px; font-size: 18px; min-height: 52px; cursor: pointer; }
.confirm-btn:disabled { background: #ef9a9a; }
</style>
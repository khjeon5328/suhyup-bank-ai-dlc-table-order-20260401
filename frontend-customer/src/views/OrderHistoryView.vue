<template>
  <div class="history-page">
    <h1 class="page-title">주문 내역</h1>
    <div v-if="orderStore.isLoading" class="loading">불러오는 중...</div>
    <div v-else-if="orderStore.currentOrders.length === 0" class="empty">주문 내역이 없습니다</div>
    <div v-else class="order-list" data-testid="order-list">
      <OrderCard v-for="order in orderStore.currentOrders" :key="order.id" :order="order" />
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useOrderStore } from '../stores/orderStore'
import OrderCard from '../components/OrderCard.vue'

const orderStore = useOrderStore()
onMounted(() => { orderStore.fetchOrders() })
</script>

<style scoped>
.history-page { padding: 16px; }
.page-title { font-size: 20px; margin-bottom: 16px; }
.loading, .empty { text-align: center; padding: 40px; color: #999; }
.order-list { display: flex; flex-direction: column; gap: 12px; }
</style>
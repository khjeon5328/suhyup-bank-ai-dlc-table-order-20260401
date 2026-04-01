<template>
  <div class="order-card" :data-testid="`order-card-${order.id}`">
    <div class="order-header">
      <span class="order-no">{{ order.order_no }}</span>
      <OrderStatusBadge :status="order.status" />
    </div>
    <p class="order-time">{{ formatDateTime(order.created_at) }}</p>
    <div class="order-items">
      <div v-for="item in order.items" :key="item.id" class="order-item">
        <span>{{ item.menu_name }} x{{ item.quantity }}</span>
        <span>{{ formatPrice(item.subtotal) }}</span>
      </div>
    </div>
    <div class="order-total">
      <span>합계</span>
      <span class="total-amount">{{ formatPrice(order.total_amount) }}</span>
    </div>
  </div>
</template>

<script setup>
import { formatPrice, formatDateTime } from '../utils/formatters'
import OrderStatusBadge from './OrderStatusBadge.vue'
defineProps({ order: Object })
</script>

<style scoped>
.order-card { background: #fff; border-radius: 12px; padding: 16px; }
.order-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px; }
.order-no { font-weight: 700; font-size: 15px; }
.order-time { font-size: 13px; color: #999; margin-bottom: 12px; }
.order-items { border-top: 1px solid #f0f0f0; padding-top: 8px; }
.order-item { display: flex; justify-content: space-between; padding: 4px 0; font-size: 14px; }
.order-total { display: flex; justify-content: space-between; border-top: 1px solid #f0f0f0; padding-top: 8px; margin-top: 8px; font-size: 16px; }
.total-amount { font-weight: 700; color: #1976d2; }
</style>
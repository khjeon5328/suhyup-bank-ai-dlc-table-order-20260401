<template>
  <div class="table-card" :data-testid="`table-card-${group.tableId}`">
    <div class="card-header">
      <h3>테이블 {{ group.tableId }}</h3>
      <span class="total">{{ formatPrice(group.totalAmount) }}</span>
    </div>
    <div class="order-list">
      <div v-for="order in group.orders.slice(0, 5)" :key="order.id" class="order-row"
           :class="{ 'new-order': order.status === 'pending' }" @click="$emit('view-detail', order)"
           :data-testid="`order-row-${order.id}`">
        <span class="order-no">{{ order.order_no }}</span>
        <OrderStatusBadge :status="order.status" />
        <div class="order-actions">
          <button v-if="order.status !== 'completed'" class="action-btn status-btn"
                  @click.stop="$emit('change-status', order)" :data-testid="`status-btn-${order.id}`">
            {{ order.status === 'pending' ? '준비중' : '완료' }}
          </button>
          <button v-if="isOwner" class="action-btn delete-btn"
                  @click.stop="$emit('delete-order', order)" :data-testid="`delete-btn-${order.id}`">삭제</button>
        </div>
      </div>
      <p v-if="group.orders.length > 5" class="more">+{{ group.orders.length - 5 }}건 더</p>
    </div>
    <div class="card-footer">
      <button class="footer-btn" @click="$emit('end-session', group.tableId)" :data-testid="`end-session-${group.tableId}`">이용 완료</button>
      <button class="footer-btn" @click="$emit('view-history', group.tableId)" :data-testid="`history-${group.tableId}`">과거 내역</button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '../stores/authStore'
import OrderStatusBadge from './OrderStatusBadge.vue'
defineProps({ group: Object })
defineEmits(['view-detail', 'change-status', 'delete-order', 'end-session', 'view-history'])
const auth = useAuthStore()
const isOwner = computed(() => auth.isOwner)
function formatPrice(n) { return `${Number(n).toLocaleString('ko-KR')}원` }
</script>

<style scoped>
.table-card { background: #fff; border-radius: 12px; overflow: hidden; box-shadow: 0 1px 4px rgba(0,0,0,0.08); }
.card-header { display: flex; justify-content: space-between; align-items: center; padding: 16px; background: #1a237e; color: #fff; }
.card-header h3 { font-size: 16px; }
.total { font-size: 18px; font-weight: 700; }
.order-list { padding: 8px 16px; }
.order-row { display: flex; align-items: center; gap: 8px; padding: 10px 0; border-bottom: 1px solid #f0f0f0; cursor: pointer; }
.order-row:last-child { border-bottom: none; }
.new-order { animation: highlight 2s ease-out; }
@keyframes highlight { from { background: #fff9c4; } to { background: transparent; } }
.order-no { font-weight: 600; font-size: 13px; min-width: 120px; }
.order-actions { margin-left: auto; display: flex; gap: 4px; }
.action-btn { padding: 6px 12px; border: none; border-radius: 6px; font-size: 12px; cursor: pointer; min-height: 32px; }
.status-btn { background: #e3f2fd; color: #1565c0; }
.delete-btn { background: #ffebee; color: #c62828; }
.more { text-align: center; color: #999; font-size: 13px; padding: 8px; }
.card-footer { display: flex; border-top: 1px solid #f0f0f0; }
.footer-btn { flex: 1; padding: 12px; background: none; border: none; font-size: 13px; cursor: pointer; color: #555; min-height: 44px; }
.footer-btn:first-child { border-right: 1px solid #f0f0f0; }
.footer-btn:hover { background: #f5f5f5; }
</style>
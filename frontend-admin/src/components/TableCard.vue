<template>
  <div class="table-card" :class="{ 'has-orders': group.orders.length > 0, 'has-pending': hasPending }"
       :data-testid="`table-card-${group.tableNo}`">
    <div class="card-header">
      <div class="table-badge">{{ group.tableNo }}</div>
      <div class="header-info">
        <h3>테이블 {{ group.tableNo }}</h3>
        <span class="order-count">주문 {{ group.orders.length }}건</span>
      </div>
      <span class="total">{{ formatPrice(group.totalAmount) }}</span>
    </div>

    <div class="card-body">
      <div v-if="group.orders.length === 0" class="no-orders">
        <span class="empty-icon">🪑</span>
        <p>대기 중</p>
      </div>
      <div v-else class="order-list">
        <div v-for="order in group.orders.slice(0, 4)" :key="order.id" class="order-row"
             :class="{ 'new-order': order.status === 'pending' }" @click="$emit('view-detail', order)">
          <div class="order-info">
            <span class="order-id">#{{ order.id }}</span>
            <OrderStatusBadge :status="order.status" />
          </div>
          <div class="order-items-preview">
            {{ getItemsPreview(order) }}
          </div>
          <div class="order-amount">{{ formatPrice(order.total_amount) }}</div>
          <div class="order-actions">
            <button v-if="order.status !== 'completed'" class="action-btn status-btn"
                    @click.stop="$emit('change-status', order)">
              {{ order.status === 'pending' ? '▶ 준비' : '✓ 완료' }}
            </button>
            <button v-if="isOwner" class="action-btn delete-btn"
                    @click.stop="$emit('delete-order', order)">✕</button>
          </div>
        </div>
        <p v-if="group.orders.length > 4" class="more">+{{ group.orders.length - 4 }}건 더보기</p>
      </div>
    </div>

    <div class="card-footer">
      <button class="footer-btn end-btn" @click="$emit('end-session', group.tableNo)">🔄 이용 완료</button>
      <button class="footer-btn history-btn" @click="$emit('view-history', group.tableNo)">📋 과거 내역</button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '../stores/authStore'
import OrderStatusBadge from './OrderStatusBadge.vue'

const props = defineProps({ group: Object })
defineEmits(['view-detail', 'change-status', 'delete-order', 'end-session', 'view-history'])

const auth = useAuthStore()
const isOwner = computed(() => auth.isOwner)
const hasPending = computed(() => props.group.orders.some(o => o.status === 'pending'))

function formatPrice(n) { return `${Number(n).toLocaleString('ko-KR')}원` }
function getItemsPreview(order) {
  if (!order.items?.length) return ''
  const first = order.items[0].menu_name
  return order.items.length > 1 ? `${first} 외 ${order.items.length - 1}건` : first
}
</script>

<style scoped>
.table-card { background: #fff; border-radius: 16px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.06); border: 2px solid transparent; transition: border-color 0.3s; }
.table-card.has-pending { border-color: #ff9800; }
.table-card.has-orders { border-color: #1a237e; }

.card-header { display: flex; align-items: center; gap: 12px; padding: 16px; background: linear-gradient(135deg, #1a237e, #283593); color: #fff; }
.table-badge { width: 40px; height: 40px; border-radius: 50%; background: rgba(255,255,255,0.2); display: flex; align-items: center; justify-content: center; font-size: 18px; font-weight: 800; }
.header-info { flex: 1; }
.header-info h3 { font-size: 15px; font-weight: 600; }
.order-count { font-size: 12px; opacity: 0.8; }
.total { font-size: 20px; font-weight: 800; }

.card-body { min-height: 100px; }
.no-orders { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 32px; color: #bbb; }
.empty-icon { font-size: 32px; margin-bottom: 8px; }
.no-orders p { font-size: 14px; }

.order-list { padding: 8px 12px; }
.order-row { display: flex; align-items: center; gap: 8px; padding: 10px 8px; border-bottom: 1px solid #f5f5f5; cursor: pointer; border-radius: 8px; transition: background 0.15s; }
.order-row:hover { background: #f8f9ff; }
.order-row:last-child { border-bottom: none; }
.new-order { animation: pulse 2s ease-out; }
@keyframes pulse { 0% { background: #fff3e0; } 100% { background: transparent; } }

.order-info { display: flex; align-items: center; gap: 6px; min-width: 100px; }
.order-id { font-weight: 700; font-size: 13px; color: #333; }
.order-items-preview { flex: 1; font-size: 12px; color: #888; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.order-amount { font-weight: 700; font-size: 13px; color: #1a237e; min-width: 70px; text-align: right; }

.order-actions { display: flex; gap: 4px; }
.action-btn { padding: 4px 10px; border: none; border-radius: 6px; font-size: 11px; cursor: pointer; min-height: 28px; font-weight: 600; }
.status-btn { background: #e8eaf6; color: #1a237e; }
.status-btn:hover { background: #c5cae9; }
.delete-btn { background: #ffebee; color: #c62828; }
.delete-btn:hover { background: #ffcdd2; }

.more { text-align: center; color: #999; font-size: 12px; padding: 8px; }

.card-footer { display: flex; border-top: 1px solid #f0f0f0; }
.footer-btn { flex: 1; padding: 12px; background: none; border: none; font-size: 13px; cursor: pointer; color: #555; min-height: 44px; font-weight: 500; transition: background 0.15s; }
.footer-btn:first-child { border-right: 1px solid #f0f0f0; }
.footer-btn:hover { background: #f5f5f5; }
</style>

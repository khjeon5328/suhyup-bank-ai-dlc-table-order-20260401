<template>
  <div v-if="visible" class="modal-overlay" @click.self="$emit('close')" data-testid="order-detail-modal">
    <div class="modal-content">
      <div class="modal-header">
        <h2>주문 상세 — {{ order.order_no }}</h2>
        <button class="close-btn" @click="$emit('close')" data-testid="modal-close">✕</button>
      </div>
      <div class="modal-body">
        <p><strong>테이블:</strong> {{ order.table_id }}</p>
        <p><strong>시각:</strong> {{ new Date(order.created_at).toLocaleString('ko-KR') }}</p>
        <p><strong>상태:</strong> <OrderStatusBadge :status="order.status" /></p>
        <table class="items-table">
          <thead><tr><th>메뉴</th><th>수량</th><th>단가</th><th>소계</th></tr></thead>
          <tbody>
            <tr v-for="item in order.items" :key="item.id">
              <td>{{ item.menu_name }}</td><td>{{ item.quantity }}</td>
              <td>{{ item.unit_price?.toLocaleString() }}원</td><td>{{ item.subtotal?.toLocaleString() }}원</td>
            </tr>
          </tbody>
        </table>
        <p class="total"><strong>총 금액:</strong> {{ order.total_amount?.toLocaleString() }}원</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import OrderStatusBadge from '@/components/OrderStatusBadge.vue'
defineProps({ order: Object, visible: Boolean })
defineEmits(['close'])
</script>

<style scoped>
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 200; }
.modal-content { background: #fff; border-radius: 12px; width: 90%; max-width: 500px; max-height: 80vh; overflow-y: auto; }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 16px 20px; border-bottom: 1px solid #eee; }
.modal-header h2 { font-size: 18px; }
.close-btn { background: none; border: none; font-size: 20px; cursor: pointer; padding: 4px; }
.modal-body { padding: 20px; }
.modal-body p { margin-bottom: 8px; font-size: 14px; }
.items-table { width: 100%; border-collapse: collapse; margin: 16px 0; }
.items-table th, .items-table td { padding: 8px; text-align: left; border-bottom: 1px solid #f0f0f0; font-size: 14px; }
.items-table th { font-weight: 600; color: #555; }
.total { font-size: 18px; text-align: right; margin-top: 12px; }
</style>
<template>
  <div class="dashboard">
    <h1>주문 모니터링</h1>
    <div v-if="orderStore.isLoading" class="loading">불러오는 중...</div>
    <div v-else-if="orderStore.orders.length === 0" class="empty">현재 주문이 없습니다</div>
    <div v-else class="table-grid" data-testid="table-grid">
      <TableCard v-for="group in orderStore.ordersByTable" :key="group.tableId" :group="group"
                 @view-detail="openDetail" @change-status="changeStatus" @delete-order="confirmDelete"
                 @end-session="confirmEndSession" @view-history="openHistory" />
    </div>
    <OrderDetailModal v-if="selectedOrder" :order="selectedOrder" :visible="showDetail"
                      @close="showDetail = false" />
    <OrderHistoryModal v-if="showHistoryModal" :storeId="auth.storeId" :tableId="historyTableId"
                       :visible="showHistoryModal" @close="showHistoryModal = false" />
    <ConfirmDialog v-if="confirmAction" :message="confirmMessage" @confirm="executeConfirm" @cancel="confirmAction = null" />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '../stores/authStore'
import { useOrderStore } from '../stores/orderStore'
import { tableService } from '../services/tableService'
import TableCard from '../components/TableCard.vue'
import OrderDetailModal from '../components/OrderDetailModal.vue'
import OrderHistoryModal from '../components/OrderHistoryModal.vue'
import ConfirmDialog from '../components/ConfirmDialog.vue'

const auth = useAuthStore()
const orderStore = useOrderStore()
const selectedOrder = ref(null); const showDetail = ref(false)
const showHistoryModal = ref(false); const historyTableId = ref(null)
const confirmAction = ref(null); const confirmMessage = ref('')
let pendingData = null

function openDetail(order) { selectedOrder.value = order; showDetail.value = true }
function openHistory(tableId) { historyTableId.value = tableId; showHistoryModal.value = true }

function changeStatus(order) {
  const next = order.status === 'pending' ? 'preparing' : 'completed'
  confirmMessage.value = `주문 ${order.order_no}을 "${next === 'preparing' ? '준비중' : '완료'}"으로 변경하시겠습니까?`
  confirmAction.value = 'changeStatus'; pendingData = { orderId: order.id, status: next }
}

function confirmDelete(order) {
  confirmMessage.value = `주문 ${order.order_no}을 삭제하시겠습니까?`
  confirmAction.value = 'delete'; pendingData = { orderId: order.id }
}

function confirmEndSession(tableId) {
  confirmMessage.value = '이 테이블을 이용 완료 처리하시겠습니까?'
  confirmAction.value = 'endSession'; pendingData = { tableId }
}

async function executeConfirm() {
  try {
    if (confirmAction.value === 'changeStatus') await orderStore.updateStatus(pendingData.orderId, pendingData.status)
    else if (confirmAction.value === 'delete') await orderStore.deleteOrder(pendingData.orderId)
    else if (confirmAction.value === 'endSession') {
      await tableService.endSession(auth.storeId, pendingData.tableId)
      await orderStore.fetchOrders()
    }
  } catch (e) { alert(e.response?.data?.detail || '처리에 실패했습니다.') }
  confirmAction.value = null; pendingData = null
}

onMounted(() => { orderStore.fetchOrders(); orderStore.connectSSE() })
onUnmounted(() => { orderStore.disconnectSSE() })
</script>

<style scoped>
.dashboard h1 { margin-bottom: 20px; font-size: 22px; }
.loading, .empty { text-align: center; padding: 60px; color: #999; }
.table-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 16px; }
</style>
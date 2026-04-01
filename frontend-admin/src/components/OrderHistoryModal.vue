<template>
  <div v-if="visible" class="modal-overlay" @click.self="$emit('close')" data-testid="history-modal">
    <div class="modal-content">
      <div class="modal-header">
        <h2>과거 주문 내역 — 테이블 {{ tableNo }}</h2>
        <button class="close-btn" @click="$emit('close')">✕</button>
      </div>
      <div class="filters">
        <input type="date" v-model="dateFrom" data-testid="history-date-from" />
        <span>~</span>
        <input type="date" v-model="dateTo" data-testid="history-date-to" />
        <button @click="loadHistory" data-testid="history-search">조회</button>
      </div>
      <div class="modal-body">
        <div v-if="loading" class="loading">불러오는 중...</div>
        <div v-else-if="history.length === 0" class="empty">내역이 없습니다</div>
        <div v-else>
          <div v-for="h in history" :key="h.id" class="history-item">
            <div class="history-header">
              <span class="order-no">{{ h.order_no }}</span>
              <span class="amount">{{ h.total_amount?.toLocaleString() }}원</span>
            </div>
            <p class="time">주문: {{ new Date(h.ordered_at).toLocaleString('ko-KR') }} | 완료: {{ new Date(h.archived_at).toLocaleString('ko-KR') }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { tableService } from '@/services/tableService'
const props = defineProps({ storeCode: String, tableNo: Number, visible: Boolean })
defineEmits(['close'])
const history = ref([]); const loading = ref(false)
const dateFrom = ref(''); const dateTo = ref('')

async function loadHistory() {
  loading.value = true
  try { history.value = await tableService.getHistory(props.storeCode, props.tableNo, dateFrom.value || null, dateTo.value || null) }
  catch { history.value = [] }
  finally { loading.value = false }
}
onMounted(loadHistory)
</script>

<style scoped>
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 200; }
.modal-content { background: #fff; border-radius: 12px; width: 90%; max-width: 600px; max-height: 80vh; overflow-y: auto; }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 16px 20px; border-bottom: 1px solid #eee; }
.close-btn { background: none; border: none; font-size: 20px; cursor: pointer; }
.filters { display: flex; align-items: center; gap: 8px; padding: 12px 20px; border-bottom: 1px solid #eee; }
.filters input { padding: 8px; border: 1px solid #ddd; border-radius: 6px; }
.filters button { padding: 8px 16px; background: #1a237e; color: #fff; border: none; border-radius: 6px; cursor: pointer; }
.modal-body { padding: 16px 20px; }
.loading, .empty { text-align: center; padding: 30px; color: #999; }
.history-item { padding: 12px 0; border-bottom: 1px solid #f0f0f0; }
.history-header { display: flex; justify-content: space-between; }
.order-no { font-weight: 600; }
.amount { font-weight: 700; color: #1a237e; }
.time { font-size: 12px; color: #999; margin-top: 4px; }
</style>
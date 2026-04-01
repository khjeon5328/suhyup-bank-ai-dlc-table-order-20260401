<template>
  <div class="table-manage">
    <div class="page-header">
      <h1>테이블 관리</h1>
      <button v-if="auth.isOwner" class="add-btn" @click="showSetup = true" data-testid="table-add-btn">+ 테이블 추가</button>
    </div>
    <div v-if="loading" class="loading">불러오는 중...</div>
    <table v-else class="data-table" data-testid="table-list">
      <thead><tr><th>번호</th><th>상태</th><th>관리</th></tr></thead>
      <tbody>
        <tr v-for="t in tables" :key="t.id" :data-testid="`table-row-${t.id}`">
          <td>{{ t.table_no }}</td>
          <td>{{ t.status }}</td>
          <td>
            <button class="action-btn" @click="handleEndSession(t)" :data-testid="`table-end-${t.id}`">이용 완료</button>
          </td>
        </tr>
      </tbody>
    </table>
    <TableSetupForm v-if="showSetup" :storeCode="auth.storeCode" @close="showSetup = false" @saved="loadTables" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import { tableService } from '@/services/tableService'
import TableSetupForm from '@/components/TableSetupForm.vue'
const auth = useAuthStore()
const tables = ref([]); const loading = ref(false); const showSetup = ref(false)

async function loadTables() {
  loading.value = true; showSetup.value = false
  try { tables.value = await tableService.getTables(auth.storeCode) } finally { loading.value = false }
}

async function handleEndSession(t) {
  if (!confirm(`테이블 ${t.table_no}을 이용 완료 처리하시겠습니까?`)) return
  try { await tableService.endSession(auth.storeCode, t.table_no); await loadTables() }
  catch (e) { alert(e.response?.data?.detail || '처리에 실패했습니다.') }
}

onMounted(loadTables)
</script>

<style scoped>
.table-manage h1 { font-size: 22px; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.add-btn { padding: 10px 20px; background: #1a237e; color: #fff; border: none; border-radius: 8px; cursor: pointer; min-height: 44px; }
.loading { text-align: center; padding: 40px; color: #999; }
.data-table { width: 100%; border-collapse: collapse; background: #fff; border-radius: 8px; overflow: hidden; }
.data-table th, .data-table td { padding: 12px 16px; text-align: left; border-bottom: 1px solid #f0f0f0; font-size: 14px; }
.data-table th { background: #f5f5f5; font-weight: 600; }
.action-btn { padding: 6px 12px; background: #e3f2fd; color: #1565c0; border: none; border-radius: 6px; cursor: pointer; min-height: 32px; }
</style>
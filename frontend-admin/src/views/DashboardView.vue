<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'
import { useTableStore } from '@/stores/table'
import { useOrderStore } from '@/stores/order'
import { usePermission } from '@/composables/usePermission'
import TableCard from '@/components/dashboard/TableCard.vue'
import OrderDetailModal from '@/components/dashboard/OrderDetailModal.vue'
import OrderHistoryPanel from '@/components/dashboard/OrderHistoryPanel.vue'
import TableSetupDialog from '@/components/dashboard/TableSetupDialog.vue'

const { t } = useI18n()
const authStore = useAuthStore()
const tableStore = useTableStore()
const orderStore = useOrderStore()
const { canSetupTable } = usePermission()

const filter = ref<'all' | 'active'>('all')
const selectedTableId = ref<number | null>(null)
const selectedTableNumber = ref<number>(0)
const showOrderDetail = ref(false)
const showHistory = ref(false)
const showTableSetup = ref(false)

const filteredTables = computed(() => {
  if (filter.value === 'active') {
    return tableStore.tables.filter((t) => t.hasActiveSession)
  }
  return tableStore.tables
})

function handleTableClick(tableId: number, tableNumber: number): void {
  selectedTableId.value = tableId
  selectedTableNumber.value = tableNumber
  tableStore.markAsRead(tableId)
  showOrderDetail.value = true
}

function handleShowHistory(tableId: number, tableNumber: number): void {
  selectedTableId.value = tableId
  selectedTableNumber.value = tableNumber
  showHistory.value = true
}

async function handleEndSession(tableId: number): Promise<void> {
  if (!authStore.storeId) return
  await tableStore.endSession(authStore.storeId, tableId)
}

onMounted(async () => {
  if (authStore.storeId) {
    await tableStore.fetchTables(authStore.storeId)
    await orderStore.fetchOrders(authStore.storeId)
  }
})
</script>

<template>
  <div>
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px">
      <h2 style="margin: 0">{{ t('dashboard.title') }}</h2>
      <div style="display: flex; gap: 8px">
        <el-radio-group v-model="filter" data-testid="table-filter">
          <el-radio-button value="all">{{ t('dashboard.filterAll') }}</el-radio-button>
          <el-radio-button value="active">{{ t('dashboard.waiting') }}</el-radio-button>
        </el-radio-group>
        <el-button v-if="canSetupTable" type="primary" data-testid="add-table-button" @click="showTableSetup = true">
          {{ t('dashboard.addTable') }}
        </el-button>
      </div>
    </div>

    <div v-if="filteredTables.length === 0" style="text-align: center; padding: 40px">
      <el-empty :description="t('common.noData')" />
    </div>

    <div v-else style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 16px">
      <TableCard
        v-for="table in filteredTables"
        :key="table.tableId"
        :table="table"
        :has-new-order="tableStore.newOrderTableIds.has(table.tableId)"
        :is-owner="authStore.isOwner"
        @click="handleTableClick(table.tableId, table.tableNumber)"
        @end-session="handleEndSession(table.tableId)"
        @show-history="handleShowHistory(table.tableId, table.tableNumber)"
      />
    </div>

    <OrderDetailModal
      :visible="showOrderDetail"
      :table-id="selectedTableId"
      :table-name="`#${selectedTableNumber}`"
      @update:visible="showOrderDetail = $event"
    />

    <OrderHistoryPanel
      :visible="showHistory"
      :table-id="selectedTableId"
      :table-number="selectedTableNumber"
      @update:visible="showHistory = $event"
    />

    <TableSetupDialog :visible="showTableSetup" @update:visible="showTableSetup = $event" />
  </div>
</template>

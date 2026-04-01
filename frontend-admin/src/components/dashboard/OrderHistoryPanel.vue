<script setup lang="ts">
import { ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'
import { useOrderStore } from '@/stores/order'
import OrderStatusBadge from '@/components/common/OrderStatusBadge.vue'

const props = defineProps<{
  visible: boolean
  tableId: number | null
  tableNumber: number
}>()

const emit = defineEmits<{ (e: 'update:visible', val: boolean): void }>()
const { t } = useI18n()
const authStore = useAuthStore()
const orderStore = useOrderStore()

const dateFrom = ref('')
const dateTo = ref('')

watch(() => props.visible, async (val) => {
  if (val && props.tableId && authStore.storeId) {
    await fetchHistory()
  }
})

async function fetchHistory(): Promise<void> {
  if (!props.tableId || !authStore.storeId) return
  await orderStore.fetchOrderHistory(
    authStore.storeId,
    props.tableId,
    dateFrom.value || undefined,
    dateTo.value || undefined,
  )
}
</script>

<template>
  <el-drawer
    :model-value="visible"
    :title="`${t('history.title')} - #${tableNumber}`"
    direction="rtl"
    size="450px"
    data-testid="order-history-panel"
    @update:model-value="emit('update:visible', $event)"
  >
    <div style="display: flex; gap: 8px; margin-bottom: 16px">
      <el-date-picker
        v-model="dateFrom"
        type="date"
        :placeholder="t('history.dateFrom')"
        value-format="YYYY-MM-DD"
        data-testid="history-date-from"
        style="flex: 1"
      />
      <el-date-picker
        v-model="dateTo"
        type="date"
        :placeholder="t('history.dateTo')"
        value-format="YYYY-MM-DD"
        data-testid="history-date-to"
        style="flex: 1"
      />
      <el-button type="primary" data-testid="history-search-button" @click="fetchHistory">
        {{ t('common.confirm') }}
      </el-button>
    </div>

    <div v-if="orderStore.orderHistory.length === 0" style="text-align: center; padding: 20px; color: #909399">
      {{ t('history.noHistory') }}
    </div>

    <el-card v-for="item in orderStore.orderHistory" :key="item.id" style="margin-bottom: 12px" shadow="never">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px">
        <span style="font-weight: 600">{{ item.orderNumber }}</span>
        <OrderStatusBadge :status="item.status" />
      </div>
      <div v-for="orderItem in item.items" :key="orderItem.id" style="display: flex; justify-content: space-between; font-size: 13px; padding: 2px 0">
        <span>{{ orderItem.menuName }} x{{ orderItem.quantity }}</span>
        <span>{{ orderItem.subtotal.toLocaleString() }}</span>
      </div>
      <div style="display: flex; justify-content: space-between; margin-top: 8px; font-size: 12px; color: #909399">
        <span>{{ t('history.archivedAt') }}: {{ item.archivedAt }}</span>
        <span style="font-weight: 600">{{ item.totalAmount.toLocaleString() }}</span>
      </div>
    </el-card>
  </el-drawer>
</template>

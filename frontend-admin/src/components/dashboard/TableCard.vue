<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import OrderStatusBadge from '@/components/common/OrderStatusBadge.vue'
import type { TableSummary } from '@/types/table'

defineProps<{
  table: TableSummary
  hasNewOrder: boolean
  isOwner: boolean
}>()

const emit = defineEmits<{
  (e: 'click'): void
  (e: 'endSession'): void
  (e: 'showHistory'): void
}>()

const { t } = useI18n()
</script>

<template>
  <el-card
    :class="{ 'pulse-animation': hasNewOrder }"
    shadow="hover"
    style="cursor: pointer; position: relative"
    data-testid="table-card"
    @click="emit('click')"
  >
    <template #header>
      <div style="display: flex; justify-content: space-between; align-items: center">
        <span style="font-weight: 600; font-size: 16px">#{{ table.tableNumber }}</span>
        <el-tag v-if="hasNewOrder" type="danger" size="small" effect="dark" data-testid="new-order-badge">
          {{ t('dashboard.newOrder') }}
        </el-tag>
      </div>
    </template>

    <div style="margin-bottom: 12px">
      <div style="display: flex; justify-content: space-between; margin-bottom: 4px">
        <span>{{ t('dashboard.totalAmount') }}</span>
        <span style="font-weight: 600">{{ table.totalOrderAmount.toLocaleString() }}</span>
      </div>
      <div style="display: flex; justify-content: space-between">
        <span>{{ t('dashboard.orderCount') }}</span>
        <span>{{ table.orderCount }}</span>
      </div>
    </div>

    <div v-if="table.latestOrders.length > 0" style="margin-bottom: 12px">
      <div v-for="order in table.latestOrders.slice(0, 3)" :key="order.id" style="display: flex; justify-content: space-between; align-items: center; padding: 4px 0">
        <span style="font-size: 12px; color: #909399">{{ order.orderNumber }}</span>
        <OrderStatusBadge :status="order.status" />
      </div>
    </div>
    <div v-else style="text-align: center; color: #909399; padding: 12px 0">
      {{ t('dashboard.noOrders') }}
    </div>

    <div style="display: flex; gap: 8px; margin-top: 8px">
      <el-button
        v-if="isOwner && table.hasActiveSession"
        size="small"
        type="warning"
        data-testid="end-session-button"
        @click.stop="emit('endSession')"
      >
        {{ t('dashboard.endSession') }}
      </el-button>
      <el-button size="small" data-testid="show-history-button" @click.stop="emit('showHistory')">
        {{ t('dashboard.history') }}
      </el-button>
    </div>
  </el-card>
</template>

<style scoped>
.pulse-animation {
  animation: pulse 2s infinite;
}
@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(245, 108, 108, 0.4); }
  70% { box-shadow: 0 0 0 10px rgba(245, 108, 108, 0); }
  100% { box-shadow: 0 0 0 0 rgba(245, 108, 108, 0); }
}
</style>

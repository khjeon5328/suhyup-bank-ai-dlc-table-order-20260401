<script setup lang="ts">
import { computed, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/authStore'
import { useOrderStore } from '@/stores/orderStore'
import { usePermission } from '@/composables/usePermission'
import { useConfirm } from '@/composables/useConfirm'
import { useAsyncAction } from '@/composables/useAsyncAction'
import OrderStatusBadge from '@/components/common/OrderStatusBadge.vue'
import OrderStatusButton from '@/components/common/OrderStatusButton.vue'
import type { OrderStatus } from '@/types/order'

const props = defineProps<{
  visible: boolean
  tableId: number | null
  tableName: string
}>()

const emit = defineEmits<{ (e: 'update:visible', val: boolean): void }>()
const { t } = useI18n()
const authStore = useAuthStore()
const orderStore = useOrderStore()
const { canDeleteOrder } = usePermission()
const { confirm } = useConfirm()
const { loading, execute } = useAsyncAction()

const orders = computed(() => {
  if (!props.tableId) return []
  return orderStore.ordersByTable.get(props.tableId) ?? []
})

watch(() => props.visible, async (val) => {
  if (val && props.tableId && authStore.storeId) {
    await orderStore.fetchOrders(authStore.storeId, props.tableId)
  }
})

async function handleStatusChange(orderId: number, status: OrderStatus): Promise<void> {
  if (!authStore.storeId) return
  await execute(() => orderStore.updateOrderStatus(authStore.storeId!, orderId, status))
  ElMessage.success(t('order.statusChanged'))
}

async function handleDelete(orderId: number): Promise<void> {
  const confirmed = await confirm(t('order.deleteConfirm'))
  if (!confirmed || !authStore.storeId) return
  await execute(() => orderStore.deleteOrder(authStore.storeId!, orderId))
  ElMessage.success(t('order.deleteSuccess'))
}
</script>

<template>
  <el-dialog
    :model-value="visible"
    :title="`${t('order.detail')} - ${tableName}`"
    width="65%"
    data-testid="order-detail-modal"
    @update:model-value="emit('update:visible', $event)"
  >
    <div v-if="orders.length === 0" style="text-align: center; padding: 20px">
      {{ t('dashboard.noOrders') }}
    </div>
    <div v-else>
      <el-card v-for="order in orders" :key="order.id" style="margin-bottom: 12px" shadow="never">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px">
          <div>
            <span style="font-weight: 600">{{ t('order.number') }}: {{ order.orderNumber }}</span>
            <OrderStatusBadge :status="order.status" style="margin-left: 8px" />
          </div>
          <div style="display: flex; gap: 8px">
            <OrderStatusButton :current-status="order.status" :loading="loading" @change="handleStatusChange(order.id, $event)" />
            <el-button
              v-if="canDeleteOrder"
              size="small"
              type="danger"
              data-testid="delete-order-button"
              @click="handleDelete(order.id)"
            >
              {{ t('common.delete') }}
            </el-button>
          </div>
        </div>
        <el-table :data="order.items" size="small">
          <el-table-column prop="menuName" label="Menu" />
          <el-table-column prop="quantity" label="Qty" width="60" />
          <el-table-column prop="unitPrice" label="Price" width="100">
            <template #default="{ row }">{{ row.unitPrice.toLocaleString() }}</template>
          </el-table-column>
          <el-table-column prop="subtotal" label="Subtotal" width="100">
            <template #default="{ row }">{{ row.subtotal.toLocaleString() }}</template>
          </el-table-column>
        </el-table>
        <div style="text-align: right; margin-top: 8px; font-weight: 600">
          {{ t('dashboard.totalAmount') }}: {{ order.totalAmount.toLocaleString() }}
        </div>
      </el-card>
    </div>
  </el-dialog>
</template>

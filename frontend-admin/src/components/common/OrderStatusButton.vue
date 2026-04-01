<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { OrderStatus } from '@/types/order'

const props = defineProps<{ currentStatus: OrderStatus; loading?: boolean }>()
const emit = defineEmits<{ (e: 'change', status: OrderStatus): void }>()
const { t } = useI18n()

const nextStatus = computed(() => {
  if (props.currentStatus === OrderStatus.PENDING) return OrderStatus.PREPARING
  if (props.currentStatus === OrderStatus.PREPARING) return OrderStatus.COMPLETED
  return null
})

const buttonText = computed(() => {
  if (props.currentStatus === OrderStatus.PENDING) return t('order.startPreparing')
  if (props.currentStatus === OrderStatus.PREPARING) return t('order.markComplete')
  return ''
})

function handleClick(): void {
  if (nextStatus.value) {
    emit('change', nextStatus.value)
  }
}
</script>

<template>
  <el-button
    v-if="nextStatus"
    :type="currentStatus === OrderStatus.PENDING ? 'primary' : 'success'"
    :loading="loading"
    size="small"
    data-testid="order-status-button"
    @click="handleClick"
  >
    {{ buttonText }}
  </el-button>
</template>

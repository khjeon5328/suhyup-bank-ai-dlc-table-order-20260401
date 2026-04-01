<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { OrderStatus } from '@/types/order'

const props = defineProps<{ status: OrderStatus }>()
const { t } = useI18n()

const tagType = computed(() => {
  switch (props.status) {
    case OrderStatus.PENDING: return 'warning'
    case OrderStatus.PREPARING: return '' as const
    case OrderStatus.COMPLETED: return 'success'
    default: return 'info'
  }
})

const label = computed(() => {
  switch (props.status) {
    case OrderStatus.PENDING: return t('order.pending')
    case OrderStatus.PREPARING: return t('order.preparing')
    case OrderStatus.COMPLETED: return t('order.completed')
    default: return props.status
  }
})
</script>

<template>
  <el-tag :type="tagType" size="small" data-testid="order-status-badge">{{ label }}</el-tag>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { sseService } from '@/services/sseService'

const { t } = useI18n()

const status = computed(() => sseService.status)

const color = computed(() => {
  switch (status.value) {
    case 'connected': return '#67c23a'
    case 'reconnecting': return '#e6a23c'
    case 'disconnected': return '#f56c6c'
    default: return '#909399'
  }
})

const tooltip = computed(() => {
  switch (status.value) {
    case 'connected': return t('sse.connected')
    case 'reconnecting': return t('sse.reconnecting')
    case 'disconnected': return t('sse.disconnected')
    default: return ''
  }
})
</script>

<template>
  <el-tooltip :content="tooltip" placement="bottom">
    <span
      data-testid="sse-status-indicator"
      :style="{
        display: 'inline-block',
        width: '10px',
        height: '10px',
        borderRadius: '50%',
        backgroundColor: color,
      }"
    />
  </el-tooltip>
</template>

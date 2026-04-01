<template>
  <span class="status-badge" :class="status" :data-testid="`status-badge-${status}`">{{ label }}</span>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({ status: String })
const labels = { pending: '대기중', preparing: '준비중', completed: '완료' }
const label = computed(() => labels[props.status] || props.status)
</script>

<style scoped>
.status-badge { padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; }
.pending { background: #fff3e0; color: #e65100; }
.preparing { background: #e3f2fd; color: #1565c0; }
.completed { background: #e8f5e9; color: #2e7d32; }
</style>
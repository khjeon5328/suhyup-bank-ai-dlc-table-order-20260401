<template>
  <span class="badge" :class="status">{{ labels[status] || status }}</span>
</template>
<script setup>
defineProps({ status: String })
const labels = { pending: '대기중', preparing: '준비중', completed: '완료' }
</script>
<style scoped>
.badge { padding: 3px 8px; border-radius: 10px; font-size: 11px; font-weight: 600; }
.pending { background: #fff3e0; color: #e65100; }
.preparing { background: #e3f2fd; color: #1565c0; }
.completed { background: #e8f5e9; color: #2e7d32; }
</style>
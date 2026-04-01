<template>
  <div class="category-tabs" data-testid="category-tabs">
    <button class="tab" :class="{ active: !activeId }" @click="$emit('select', null)" data-testid="category-all">전체</button>
    <button v-for="cat in categories" :key="cat.id" class="tab" :class="{ active: activeId === cat.id }"
            @click="$emit('select', cat.id)" :data-testid="`category-${cat.id}`">{{ cat.name }}</button>
  </div>
</template>

<script setup>
defineProps({ categories: Array, activeId: Number })
defineEmits(['select'])
</script>

<style scoped>
.category-tabs { display: flex; gap: 8px; overflow-x: auto; padding: 8px 0; -webkit-overflow-scrolling: touch; }
.tab { padding: 10px 20px; border: 1px solid #ddd; border-radius: 20px; background: #fff; font-size: 14px; white-space: nowrap; min-height: 44px; cursor: pointer; }
.tab.active { background: #1976d2; color: #fff; border-color: #1976d2; }
</style>
<template>
  <div class="menu-card" @click="$emit('click')" :data-testid="`menu-card-${menu.id}`">
    <div class="card-image">
      <img v-if="menu.image_url" :src="menu.image_url" :alt="menu.name" loading="lazy" @error="onImgError" />
      <div v-else class="placeholder">🍽</div>
    </div>
    <div class="card-body">
      <p class="card-name">{{ menu.name }}</p>
      <p class="card-price">{{ formatPrice(menu.price) }}</p>
    </div>
    <button class="add-btn" @click.stop="$emit('add-to-cart')" :data-testid="`menu-add-${menu.id}`">추가</button>
  </div>
</template>

<script setup>
import { formatPrice } from '../utils/formatters'
defineProps({ menu: Object })
defineEmits(['click', 'add-to-cart'])
function onImgError(e) { e.target.style.display = 'none' }
</script>

<style scoped>
.menu-card { background: #fff; border-radius: 12px; overflow: hidden; box-shadow: 0 1px 4px rgba(0,0,0,0.1); display: flex; flex-direction: column; cursor: pointer; }
.card-image { height: 120px; background: #f0f0f0; display: flex; align-items: center; justify-content: center; overflow: hidden; }
.card-image img { width: 100%; height: 100%; object-fit: cover; }
.placeholder { font-size: 40px; }
.card-body { padding: 10px; flex: 1; }
.card-name { font-size: 14px; font-weight: 600; margin-bottom: 4px; }
.card-price { font-size: 15px; color: #1976d2; font-weight: 700; }
.add-btn { margin: 0 10px 10px; padding: 10px; background: #1976d2; color: #fff; border: none; border-radius: 8px; font-size: 14px; min-height: 44px; cursor: pointer; }
</style>
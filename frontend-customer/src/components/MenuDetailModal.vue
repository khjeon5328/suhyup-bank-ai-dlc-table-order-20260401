<template>
  <div v-if="visible" class="modal-overlay" @click.self="$emit('close')" data-testid="menu-detail-modal">
    <div class="modal-content">
      <button class="close-btn" @click="$emit('close')" data-testid="modal-close">✕</button>
      <img v-if="menu.image_url" :src="menu.image_url" :alt="menu.name" class="detail-image" />
      <div class="detail-body">
        <h2 class="detail-name">{{ menu.name }}</h2>
        <p class="detail-price">{{ formatPrice(menu.price) }}</p>
        <p v-if="menu.description" class="detail-desc">{{ menu.description }}</p>
        <button class="add-btn" @click="$emit('add-to-cart', menu)" data-testid="modal-add-to-cart">장바구니에 추가</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { formatPrice } from '../utils/formatters'
defineProps({ menu: Object, visible: Boolean })
defineEmits(['close', 'add-to-cart'])
</script>

<style scoped>
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 200; }
.modal-content { background: #fff; border-radius: 16px; width: 90%; max-width: 420px; max-height: 85vh; overflow-y: auto; position: relative; }
.close-btn { position: absolute; top: 12px; right: 12px; background: rgba(0,0,0,0.4); color: #fff; border: none; border-radius: 50%; width: 36px; height: 36px; font-size: 18px; cursor: pointer; z-index: 1; }
.detail-image { width: 100%; height: 240px; object-fit: cover; }
.detail-body { padding: 20px; }
.detail-name { font-size: 20px; margin-bottom: 8px; }
.detail-price { font-size: 22px; color: #1976d2; font-weight: 700; margin-bottom: 12px; }
.detail-desc { font-size: 14px; color: #666; line-height: 1.5; margin-bottom: 20px; }
.add-btn { width: 100%; padding: 16px; background: #1976d2; color: #fff; border: none; border-radius: 8px; font-size: 16px; min-height: 52px; cursor: pointer; }
</style>
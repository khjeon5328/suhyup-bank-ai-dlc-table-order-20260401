<template>
  <div class="cart-item" :data-testid="`cart-item-${item.menuId}`">
    <div class="item-info">
      <p class="item-name">{{ item.name }}</p>
      <p class="item-price">{{ formatPrice(item.price) }}</p>
    </div>
    <div class="item-controls">
      <button class="qty-btn" @click="$emit('decrease')" :data-testid="`cart-decrease-${item.menuId}`">−</button>
      <span class="qty" :data-testid="`cart-qty-${item.menuId}`">{{ item.quantity }}</span>
      <button class="qty-btn" @click="$emit('increase')" :data-testid="`cart-increase-${item.menuId}`">+</button>
    </div>
    <div class="item-subtotal">
      <p>{{ formatPrice(item.price * item.quantity) }}</p>
      <button class="remove-btn" @click="$emit('remove')" :data-testid="`cart-remove-${item.menuId}`">삭제</button>
    </div>
  </div>
</template>

<script setup>
import { formatPrice } from '../utils/formatters'
defineProps({ item: Object })
defineEmits(['increase', 'decrease', 'remove'])
</script>

<style scoped>
.cart-item { display: flex; align-items: center; gap: 12px; background: #fff; border-radius: 10px; padding: 14px; margin-bottom: 8px; }
.item-info { flex: 1; }
.item-name { font-size: 15px; font-weight: 600; }
.item-price { font-size: 13px; color: #888; }
.item-controls { display: flex; align-items: center; gap: 12px; }
.qty-btn { width: 36px; height: 36px; border: 1px solid #ddd; border-radius: 50%; background: #fff; font-size: 18px; cursor: pointer; display: flex; align-items: center; justify-content: center; min-width: 44px; min-height: 44px; }
.qty { font-size: 16px; font-weight: 600; min-width: 24px; text-align: center; }
.item-subtotal { text-align: right; min-width: 80px; }
.item-subtotal p { font-weight: 700; font-size: 15px; }
.remove-btn { background: none; border: none; color: #f44336; font-size: 12px; cursor: pointer; margin-top: 4px; padding: 4px; min-height: 44px; }
</style>
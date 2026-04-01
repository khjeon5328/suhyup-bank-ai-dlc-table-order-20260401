<template>
  <div class="cart-page">
    <h1 class="page-title">장바구니</h1>
    <div v-if="cartStore.isEmpty" class="empty" data-testid="cart-empty">
      <p>장바구니가 비어있습니다</p>
      <router-link to="/" class="go-menu">메뉴 보러가기</router-link>
    </div>
    <template v-else>
      <div class="cart-list" data-testid="cart-list">
        <CartItemRow v-for="item in cartStore.items" :key="item.menuId" :item="item"
                     @increase="cartStore.increaseQuantity(item.menuId)"
                     @decrease="cartStore.decreaseQuantity(item.menuId)"
                     @remove="cartStore.removeItem(item.menuId)" />
      </div>
      <div class="cart-footer">
        <button class="clear-btn" @click="cartStore.clearCart()" data-testid="cart-clear">전체 비우기</button>
        <div class="total" data-testid="cart-total">
          <span>총 금액</span>
          <span class="total-amount">{{ formatPrice(cartStore.totalAmount) }}</span>
        </div>
        <router-link to="/order/confirm" class="order-btn" data-testid="cart-order-btn">주문하기</router-link>
      </div>
    </template>
  </div>
</template>

<script setup>
import { useCartStore } from '../stores/cartStore'
import { formatPrice } from '../utils/formatters'
import CartItemRow from '../components/CartItemRow.vue'
const cartStore = useCartStore()
</script>

<style scoped>
.cart-page { padding: 16px; }
.page-title { font-size: 20px; margin-bottom: 16px; }
.empty { text-align: center; padding: 60px 0; color: #999; }
.go-menu { display: inline-block; margin-top: 16px; color: #1976d2; text-decoration: none; }
.cart-list { margin-bottom: 16px; }
.cart-footer { background: #fff; border-radius: 12px; padding: 16px; }
.clear-btn { background: none; border: 1px solid #ddd; border-radius: 8px; padding: 10px 16px; color: #666; font-size: 14px; min-height: 44px; cursor: pointer; margin-bottom: 16px; }
.total { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; font-size: 18px; }
.total-amount { font-weight: 700; color: #1976d2; font-size: 22px; }
.order-btn { display: block; text-align: center; padding: 16px; background: #1976d2; color: #fff; border-radius: 8px; font-size: 18px; text-decoration: none; min-height: 52px; }
</style>
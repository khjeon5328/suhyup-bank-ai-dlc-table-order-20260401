<template>
  <div class="app">
    <div v-if="sseConnectionLost" class="connection-banner" data-testid="sse-lost-banner">
      연결이 끊어졌습니다. <button @click="reload">새로고침</button>
    </div>
    <router-view />
    <nav v-if="isAuthenticated" class="bottom-nav" data-testid="bottom-nav">
      <router-link to="/" class="nav-item" data-testid="nav-menu">
        <span class="nav-icon">🍽</span>
        <span class="nav-label">메뉴</span>
      </router-link>
      <router-link to="/cart" class="nav-item" data-testid="nav-cart">
        <span class="nav-icon">🛒</span>
        <span class="nav-label">장바구니</span>
        <span v-if="cartCount > 0" class="badge" data-testid="cart-badge">{{ cartCount }}</span>
      </router-link>
      <router-link to="/orders" class="nav-item" data-testid="nav-orders">
        <span class="nav-icon">📋</span>
        <span class="nav-label">주문내역</span>
      </router-link>
    </nav>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from './stores/authStore'
import { useCartStore } from './stores/cartStore'
import { useOrderStore } from './stores/orderStore'

const authStore = useAuthStore()
const cartStore = useCartStore()
const orderStore = useOrderStore()

const isAuthenticated = computed(() => authStore.isAuthenticated)
const cartCount = computed(() => cartStore.totalItems)
const sseConnectionLost = computed(() => orderStore.sseConnectionLost)

function reload() { window.location.reload() }
</script>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f5f5f5; }
.app { padding-bottom: 70px; min-height: 100vh; }
.connection-banner { background: #f44336; color: #fff; text-align: center; padding: 10px; font-size: 14px; }
.connection-banner button { background: #fff; color: #f44336; border: none; border-radius: 4px; padding: 4px 12px; margin-left: 8px; cursor: pointer; font-size: 14px; }
.bottom-nav {
  position: fixed; bottom: 0; left: 0; right: 0;
  display: flex; justify-content: space-around; align-items: center;
  background: #fff; border-top: 1px solid #e0e0e0;
  height: 64px; z-index: 100;
}
.nav-item {
  display: flex; flex-direction: column; align-items: center;
  text-decoration: none; color: #666; padding: 8px 16px;
  min-width: 64px; min-height: 48px; position: relative;
}
.nav-item.router-link-active { color: #1976d2; }
.nav-icon { font-size: 24px; }
.nav-label { font-size: 12px; margin-top: 2px; }
.badge {
  position: absolute; top: 2px; right: 4px;
  background: #f44336; color: #fff; border-radius: 10px;
  font-size: 11px; min-width: 18px; height: 18px;
  display: flex; align-items: center; justify-content: center; padding: 0 4px;
}
</style>
<template>
  <div class="app">
    <div v-if="orderStore.sseConnectionLost" class="connection-banner" data-testid="sse-lost-banner">
      연결이 끊어졌습니다. <button @click="() => location.reload()">새로고침</button>
    </div>
    <nav v-if="auth.isAuthenticated" class="sidebar" data-testid="sidebar">
      <div class="sidebar-header">
        <h2>테이블오더</h2>
        <span class="role-badge" :data-testid="`role-${auth.role}`">{{ auth.role === 'owner' ? '점주' : '매니저' }}</span>
      </div>
      <router-link to="/" class="nav-link" data-testid="nav-dashboard">📊 주문 모니터링</router-link>
      <router-link v-if="auth.isOwner" to="/menus" class="nav-link" data-testid="nav-menus">🍽 메뉴 관리</router-link>
      <router-link to="/tables" class="nav-link" data-testid="nav-tables">🪑 테이블 관리</router-link>
      <router-link v-if="auth.isOwner" to="/users" class="nav-link" data-testid="nav-users">👤 계정 관리</router-link>
      <button class="logout-btn" @click="handleLogout" data-testid="nav-logout">로그아웃</button>
    </nav>
    <main :class="{ 'with-sidebar': auth.isAuthenticated }">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { useAuthStore } from './stores/authStore'
import { useOrderStore } from './stores/orderStore'
import { useRouter } from 'vue-router'
const auth = useAuthStore()
const orderStore = useOrderStore()
const router = useRouter()
function handleLogout() { orderStore.disconnectSSE(); auth.logout(); router.push('/login') }
</script>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f5f5f5; }
.connection-banner { background: #f44336; color: #fff; text-align: center; padding: 10px; font-size: 14px; position: fixed; top: 0; left: 0; right: 0; z-index: 999; }
.connection-banner button { background: #fff; color: #f44336; border: none; border-radius: 4px; padding: 4px 12px; margin-left: 8px; cursor: pointer; }
.sidebar { position: fixed; left: 0; top: 0; bottom: 0; width: 220px; background: #1a237e; color: #fff; padding: 20px 0; display: flex; flex-direction: column; z-index: 100; }
.sidebar-header { padding: 0 16px 20px; border-bottom: 1px solid rgba(255,255,255,0.1); }
.sidebar-header h2 { font-size: 18px; margin-bottom: 4px; }
.role-badge { font-size: 12px; background: rgba(255,255,255,0.2); padding: 2px 8px; border-radius: 10px; }
.nav-link { display: block; padding: 14px 20px; color: rgba(255,255,255,0.8); text-decoration: none; font-size: 14px; min-height: 48px; display: flex; align-items: center; }
.nav-link:hover, .nav-link.router-link-active { background: rgba(255,255,255,0.1); color: #fff; }
.logout-btn { margin-top: auto; padding: 14px 20px; background: none; border: none; color: rgba(255,255,255,0.6); cursor: pointer; text-align: left; font-size: 14px; }
.with-sidebar { margin-left: 220px; padding: 24px; min-height: 100vh; }
</style>
<template>
  <div class="app-layout">
    <aside class="sidebar" data-testid="sidebar">
      <div class="sidebar-header">
        <h2>테이블오더</h2>
        <span class="role-badge">{{ authStore.isOwner ? '점주' : '매니저' }}</span>
      </div>
      <nav class="sidebar-nav">
        <router-link to="/" class="nav-link" data-testid="nav-dashboard">📊 주문 모니터링</router-link>
        <router-link v-if="authStore.isOwner" to="/menus" class="nav-link" data-testid="nav-menus">🍽 메뉴 관리</router-link>
        <router-link to="/tables" class="nav-link" data-testid="nav-tables">🪑 테이블 관리</router-link>
        <router-link v-if="authStore.isOwner" to="/users" class="nav-link" data-testid="nav-users">👤 계정 관리</router-link>
      </nav>
      <button class="logout-btn" @click="handleLogout" data-testid="nav-logout">로그아웃</button>
    </aside>
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
const authStore = useAuthStore()
const router = useRouter()
function handleLogout() { authStore.logout(); router.push('/login') }
</script>

<style scoped>
.app-layout { display: flex; min-height: 100vh; }
.sidebar { width: 220px; background: #1a237e; color: #fff; display: flex; flex-direction: column; position: fixed; top: 0; bottom: 0; }
.sidebar-header { padding: 20px 16px; border-bottom: 1px solid rgba(255,255,255,0.1); }
.sidebar-header h2 { font-size: 18px; margin-bottom: 4px; }
.role-badge { font-size: 12px; background: rgba(255,255,255,0.2); padding: 2px 8px; border-radius: 10px; }
.sidebar-nav { flex: 1; padding-top: 8px; }
.nav-link { display: flex; align-items: center; padding: 14px 20px; color: rgba(255,255,255,0.8); text-decoration: none; font-size: 14px; min-height: 48px; }
.nav-link:hover, .nav-link.router-link-active { background: rgba(255,255,255,0.1); color: #fff; }
.logout-btn { padding: 14px 20px; background: none; border: none; color: rgba(255,255,255,0.6); cursor: pointer; text-align: left; font-size: 14px; border-top: 1px solid rgba(255,255,255,0.1); }
.main-content { margin-left: 220px; padding: 24px; flex: 1; background: #f5f5f5; min-height: 100vh; }
</style>
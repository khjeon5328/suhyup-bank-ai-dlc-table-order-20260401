<template>
  <div id="admin-app">
    <nav v-if="auth.isAuthenticated" class="top-nav">
      <div class="nav-left">
        <router-link to="/" class="nav-link" :class="{ active: $route.path === '/' }">📊 대시보드</router-link>
        <router-link v-if="auth.isOwner" to="/menus" class="nav-link" :class="{ active: $route.path === '/menus' }">🍽 메뉴 관리</router-link>
        <router-link v-if="auth.isOwner" to="/users" class="nav-link" :class="{ active: $route.path === '/users' }">👤 사용자 관리</router-link>
      </div>
      <div class="nav-right">
        <span class="user-info">{{ auth.storeCode }} · {{ auth.username }} ({{ auth.role === 'owner' ? '점주' : '매니저' }})</span>
        <button class="logout-btn" @click="handleLogout">로그아웃</button>
      </div>
    </nav>
    <main :class="{ 'with-nav': auth.isAuthenticated }">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from './stores/authStore'
const auth = useAuthStore()
const router = useRouter()
function handleLogout() { auth.logout(); router.push('/login') }
</script>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f0f2f5; }
#admin-app { min-height: 100vh; }
.top-nav { display: flex; justify-content: space-between; align-items: center; background: #1a237e; padding: 0 20px; height: 56px; position: fixed; top: 0; left: 0; right: 0; z-index: 100; }
.nav-left { display: flex; gap: 4px; }
.nav-link { color: rgba(255,255,255,0.7); text-decoration: none; padding: 8px 16px; border-radius: 8px; font-size: 14px; transition: all 0.2s; }
.nav-link:hover { color: #fff; background: rgba(255,255,255,0.1); }
.nav-link.active { color: #fff; background: rgba(255,255,255,0.2); }
.nav-right { display: flex; align-items: center; gap: 12px; }
.user-info { color: rgba(255,255,255,0.8); font-size: 13px; }
.logout-btn { padding: 6px 14px; background: rgba(255,255,255,0.15); color: #fff; border: none; border-radius: 6px; font-size: 13px; cursor: pointer; }
.logout-btn:hover { background: rgba(255,255,255,0.25); }
main.with-nav { padding-top: 72px; padding-left: 20px; padding-right: 20px; }
</style>

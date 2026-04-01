<template>
  <div class="login-page">
    <div class="login-card">
      <h2>관리자 로그인</h2>
      <form @submit.prevent="handleLogin" data-testid="login-form">
        <div class="form-group">
          <label>매장 코드</label>
          <input v-model="storeCode" type="text" placeholder="매장 코드" data-testid="input-store-code" />
        </div>
        <div class="form-group">
          <label>아이디</label>
          <input v-model="username" type="text" placeholder="아이디" data-testid="input-username" />
        </div>
        <div class="form-group">
          <label>비밀번호</label>
          <input v-model="password" type="password" placeholder="비밀번호" data-testid="input-password" />
        </div>
        <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
        <button type="submit" :disabled="loading" data-testid="login-button">
          {{ loading ? '로그인 중...' : '로그인' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/authStore'

const router = useRouter()
const auth = useAuthStore()
const storeCode = ref('')
const username = ref('')
const password = ref('')
const loading = ref(false)
const errorMsg = ref('')

async function handleLogin() {
  if (!storeCode.value || !username.value || !password.value) {
    errorMsg.value = '모든 필드를 입력해주세요.'
    return
  }
  loading.value = true
  errorMsg.value = ''
  try {
    await auth.login(storeCode.value, username.value, password.value)
    router.push('/')
  } catch (e) {
    errorMsg.value = e.response?.status === 429
      ? '너무 많은 요청입니다. 잠시 후 다시 시도해주세요.'
      : '로그인에 실패했습니다. 정보를 확인해주세요.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page { display: flex; justify-content: center; align-items: center; min-height: 100vh; background: #f5f7fa; }
.login-card { width: 400px; background: #fff; border-radius: 12px; padding: 32px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); }
.login-card h2 { text-align: center; margin-bottom: 24px; color: #333; }
.form-group { margin-bottom: 16px; }
.form-group label { display: block; margin-bottom: 6px; font-size: 14px; color: #555; }
.form-group input { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 15px; box-sizing: border-box; }
.error { color: #f44336; font-size: 13px; margin-bottom: 12px; }
button { width: 100%; padding: 14px; background: #1976d2; color: #fff; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; }
button:disabled { background: #90caf9; }
</style>

<template>
  <div class="login-page">
    <div class="login-card">
      <h1>관리자 로그인</h1>
      <form @submit.prevent="handleLogin" data-testid="login-form">
        <div class="form-group">
          <label>매장 코드</label>
          <input v-model="storeCode" type="text" placeholder="매장 코드" data-testid="login-store-code" maxlength="50" />
        </div>
        <div class="form-group">
          <label>사용자명</label>
          <input v-model="username" type="text" placeholder="사용자명" data-testid="login-username" />
        </div>
        <div class="form-group">
          <label>비밀번호</label>
          <input v-model="password" type="password" placeholder="비밀번호" data-testid="login-password" />
        </div>
        <p v-if="error" class="error" data-testid="login-error">{{ error }}</p>
        <button type="submit" :disabled="loading" class="login-btn" data-testid="login-submit">
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
const storeCode = ref(''); const username = ref(''); const password = ref('')
const loading = ref(false); const error = ref('')

async function handleLogin() {
  error.value = ''; loading.value = true
  try {
    await auth.login(storeCode.value, username.value, password.value)
    router.push('/')
  } catch (e) {
    error.value = e.response?.data?.detail || '로그인에 실패했습니다.'
  } finally { loading.value = false }
}
</script>

<style scoped>
.login-page { display: flex; align-items: center; justify-content: center; min-height: 100vh; }
.login-card { background: #fff; border-radius: 12px; padding: 40px; width: 100%; max-width: 400px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); }
h1 { text-align: center; margin-bottom: 24px; font-size: 22px; }
.form-group { margin-bottom: 16px; }
.form-group label { display: block; margin-bottom: 6px; font-size: 14px; color: #555; }
.form-group input { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 15px; }
.error { color: #f44336; text-align: center; margin-bottom: 12px; font-size: 14px; }
.login-btn { width: 100%; padding: 14px; background: #1a237e; color: #fff; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; }
.login-btn:disabled { opacity: 0.6; }
</style>
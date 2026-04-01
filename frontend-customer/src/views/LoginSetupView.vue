<template>
  <div class="setup-page">
    <h1 class="setup-title">테이블 설정</h1>
    <form class="setup-form" @submit.prevent="handleSubmit" data-testid="setup-form">
      <div class="form-group">
        <label for="storeCode">매장 코드</label>
        <input id="storeCode" v-model="storeCode" type="text" placeholder="매장 코드 입력"
               data-testid="setup-store-code" maxlength="50" />
        <span v-if="errors.storeCode" class="error">{{ errors.storeCode }}</span>
      </div>
      <div class="form-group">
        <label for="tableNo">테이블 번호</label>
        <input id="tableNo" v-model="tableNo" type="number" placeholder="테이블 번호"
               data-testid="setup-table-no" min="1" />
        <span v-if="errors.tableNo" class="error">{{ errors.tableNo }}</span>
      </div>
      <div class="form-group">
        <label for="password">비밀번호</label>
        <input id="password" v-model="password" type="password" placeholder="비밀번호"
               data-testid="setup-password" />
        <span v-if="errors.password" class="error">{{ errors.password }}</span>
      </div>
      <p v-if="serverError" class="error server-error" data-testid="setup-error">{{ serverError }}</p>
      <button type="submit" class="submit-btn" :disabled="isLoading" data-testid="setup-submit">
        {{ isLoading ? '설정 중...' : '설정 완료' }}
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/authStore'
import { validateStoreCode, validateTableNo, validatePassword } from '../utils/validators'

const router = useRouter()
const authStore = useAuthStore()

const storeCode = ref('')
const tableNo = ref('')
const password = ref('')
const isLoading = ref(false)
const serverError = ref('')
const errors = ref({})

async function handleSubmit() {
  errors.value = {}
  serverError.value = ''
  const e1 = validateStoreCode(storeCode.value)
  const e2 = validateTableNo(tableNo.value)
  const e3 = validatePassword(password.value)
  if (e1) errors.value.storeCode = e1
  if (e2) errors.value.tableNo = e2
  if (e3) errors.value.password = e3
  if (Object.keys(errors.value).length > 0) return

  isLoading.value = true
  try {
    await authStore.login(storeCode.value, Number(tableNo.value), password.value)
    router.push('/')
  } catch (err) {
    serverError.value = err.response?.data?.detail || '로그인에 실패했습니다. 정보를 확인해 주세요.'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.setup-page { display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; padding: 24px; }
.setup-title { font-size: 24px; margin-bottom: 32px; color: #333; }
.setup-form { width: 100%; max-width: 400px; }
.form-group { margin-bottom: 20px; }
.form-group label { display: block; margin-bottom: 6px; font-size: 14px; color: #555; }
.form-group input { width: 100%; padding: 14px; border: 1px solid #ddd; border-radius: 8px; font-size: 16px; }
.error { color: #f44336; font-size: 13px; margin-top: 4px; display: block; }
.server-error { text-align: center; margin-bottom: 16px; }
.submit-btn { width: 100%; padding: 16px; background: #1976d2; color: #fff; border: none; border-radius: 8px; font-size: 18px; min-height: 52px; cursor: pointer; }
.submit-btn:disabled { background: #90caf9; }
</style>
<template>
  <div class="modal-overlay" @click.self="$emit('close')" data-testid="user-form-modal">
    <div class="modal-content">
      <h2>{{ user ? '계정 수정' : '계정 추가' }}</h2>
      <form @submit.prevent="handleSubmit" data-testid="user-form">
        <div class="form-group">
          <label>사용자명 *</label>
          <input v-model="form.username" required maxlength="50" data-testid="user-form-username" />
        </div>
        <div class="form-group">
          <label>{{ user ? '비밀번호 (변경 시에만)' : '비밀번호 *' }}</label>
          <input v-model="form.password" type="password" :required="!user" data-testid="user-form-password" />
        </div>
        <div class="form-group">
          <label>역할 *</label>
          <select v-model="form.role" required data-testid="user-form-role">
            <option value="owner">점주</option>
            <option value="manager">매니저</option>
          </select>
        </div>
        <p v-if="error" class="error">{{ error }}</p>
        <div class="form-actions">
          <button type="button" class="cancel-btn" @click="$emit('close')">취소</button>
          <button type="submit" class="submit-btn" :disabled="saving" data-testid="user-form-submit">
            {{ saving ? '저장 중...' : '저장' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { userService } from '../services/userService'
const props = defineProps({ user: Object, storeCode: String })
const emit = defineEmits(['close', 'saved'])
const form = ref({ username: '', password: '', role: 'manager' })
const saving = ref(false); const error = ref('')

onMounted(() => {
  if (props.user) { form.value = { username: props.user.username, password: '', role: props.user.role } }
})

async function handleSubmit() {
  error.value = ''; saving.value = true
  try {
    const payload = { ...form.value }
    if (props.user && !payload.password) delete payload.password
    if (props.user) await userService.updateUser(props.storeCode, props.user.id, payload)
    else await userService.createUser(props.storeCode, payload)
    emit('saved')
  } catch (e) { error.value = e.response?.data?.detail || '저장에 실패했습니다.' }
  finally { saving.value = false }
}
</script>

<style scoped>
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 200; }
.modal-content { background: #fff; border-radius: 12px; padding: 24px; width: 90%; max-width: 400px; }
h2 { margin-bottom: 20px; }
.form-group { margin-bottom: 14px; }
.form-group label { display: block; margin-bottom: 4px; font-size: 13px; color: #555; }
.form-group input, .form-group select { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px; }
.error { color: #f44336; font-size: 13px; margin-bottom: 12px; }
.form-actions { display: flex; gap: 12px; margin-top: 16px; }
.cancel-btn, .submit-btn { flex: 1; padding: 12px; border: none; border-radius: 8px; font-size: 15px; cursor: pointer; min-height: 44px; }
.cancel-btn { background: #f5f5f5; }
.submit-btn { background: #1a237e; color: #fff; }
.submit-btn:disabled { opacity: 0.6; }
</style>
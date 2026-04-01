<template>
  <div class="modal-overlay" @click.self="$emit('close')" data-testid="table-setup-modal">
    <div class="modal-content">
      <h2>테이블 추가</h2>
      <form @submit.prevent="handleSubmit" data-testid="table-setup-form">
        <div class="form-group">
          <label>테이블 번호 *</label>
          <input v-model.number="tableNo" type="number" min="1" required data-testid="table-setup-no" />
        </div>
        <div class="form-group">
          <label>비밀번호 *</label>
          <input v-model="password" type="password" required data-testid="table-setup-password" />
        </div>
        <p v-if="error" class="error">{{ error }}</p>
        <div class="form-actions">
          <button type="button" class="cancel-btn" @click="$emit('close')">취소</button>
          <button type="submit" class="submit-btn" :disabled="saving" data-testid="table-setup-submit">
            {{ saving ? '저장 중...' : '저장' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { tableService } from '../services/tableService'
const props = defineProps({ storeCode: String })
const emit = defineEmits(['close', 'saved'])
const tableNo = ref(''); const password = ref(''); const saving = ref(false); const error = ref('')

async function handleSubmit() {
  error.value = ''; saving.value = true
  try { await tableService.setupTable(props.storeCode, tableNo.value, password.value); emit('saved') }
  catch (e) { error.value = e.response?.data?.detail || '저장에 실패했습니다.' }
  finally { saving.value = false }
}
</script>

<style scoped>
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 200; }
.modal-content { background: #fff; border-radius: 12px; padding: 24px; width: 90%; max-width: 400px; }
h2 { margin-bottom: 20px; }
.form-group { margin-bottom: 14px; }
.form-group label { display: block; margin-bottom: 4px; font-size: 13px; color: #555; }
.form-group input { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px; }
.error { color: #f44336; font-size: 13px; margin-bottom: 12px; }
.form-actions { display: flex; gap: 12px; margin-top: 16px; }
.cancel-btn, .submit-btn { flex: 1; padding: 12px; border: none; border-radius: 8px; font-size: 15px; cursor: pointer; min-height: 44px; }
.cancel-btn { background: #f5f5f5; }
.submit-btn { background: #1a237e; color: #fff; }
.submit-btn:disabled { opacity: 0.6; }
</style>
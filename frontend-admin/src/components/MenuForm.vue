<template>
  <div class="modal-overlay" @click.self="$emit('close')" data-testid="menu-form-modal">
    <div class="modal-content">
      <h2>{{ menu ? '메뉴 수정' : '메뉴 추가' }}</h2>
      <form @submit.prevent="handleSubmit" data-testid="menu-form">
        <div class="form-group">
          <label>메뉴명 *</label>
          <input v-model="form.name" required maxlength="100" data-testid="menu-form-name" />
        </div>
        <div class="form-group">
          <label>가격 *</label>
          <input v-model.number="form.price" type="number" min="0" required data-testid="menu-form-price" />
        </div>
        <div class="form-group">
          <label>카테고리 *</label>
          <select v-model.number="form.category_id" required data-testid="menu-form-category">
            <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
          </select>
        </div>
        <div class="form-group">
          <label>설명</label>
          <textarea v-model="form.description" maxlength="1000" data-testid="menu-form-desc"></textarea>
        </div>
        <div class="form-group">
          <label>이미지 URL</label>
          <input v-model="form.image_url" maxlength="500" data-testid="menu-form-image" />
        </div>
        <p v-if="error" class="error">{{ error }}</p>
        <div class="form-actions">
          <button type="button" class="cancel-btn" @click="$emit('close')">취소</button>
          <button type="submit" class="submit-btn" :disabled="saving" data-testid="menu-form-submit">
            {{ saving ? '저장 중...' : '저장' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { menuService } from '@/services/menuService'
const props = defineProps({ menu: Object, categories: Array, storeCode: String })
const emit = defineEmits(['close', 'saved'])
const form = ref({ name: '', price: 0, category_id: null, description: '', image_url: '' })
const saving = ref(false); const error = ref('')

onMounted(() => {
  if (props.menu) {
    form.value = { name: props.menu.name, price: props.menu.price, category_id: props.menu.category_id,
      description: props.menu.description || '', image_url: props.menu.image_url || '' }
  } else if (props.categories?.length) { form.value.category_id = props.categories[0].id }
})

async function handleSubmit() {
  error.value = ''; saving.value = true
  try {
    if (props.menu) await menuService.updateMenu(props.storeCode, props.menu.id, form.value)
    else await menuService.createMenu(props.storeCode, form.value)
    emit('saved')
  } catch (e) { error.value = e.response?.data?.detail || '저장에 실패했습니다.' }
  finally { saving.value = false }
}
</script>

<style scoped>
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 200; }
.modal-content { background: #fff; border-radius: 12px; padding: 24px; width: 90%; max-width: 480px; }
h2 { margin-bottom: 20px; font-size: 18px; }
.form-group { margin-bottom: 14px; }
.form-group label { display: block; margin-bottom: 4px; font-size: 13px; color: #555; }
.form-group input, .form-group select, .form-group textarea { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px; }
.form-group textarea { height: 80px; resize: vertical; }
.error { color: #f44336; font-size: 13px; margin-bottom: 12px; }
.form-actions { display: flex; gap: 12px; margin-top: 16px; }
.cancel-btn, .submit-btn { flex: 1; padding: 12px; border: none; border-radius: 8px; font-size: 15px; cursor: pointer; min-height: 44px; }
.cancel-btn { background: #f5f5f5; color: #333; }
.submit-btn { background: #1a237e; color: #fff; }
.submit-btn:disabled { opacity: 0.6; }
</style>
<template>
  <div class="modal-overlay" data-testid="confirm-dialog">
    <div class="dialog">
      <p class="message">{{ message }}</p>
      <div class="actions">
        <button class="cancel-btn" @click="$emit('cancel')" data-testid="confirm-cancel">취소</button>
        <button class="confirm-btn" @click="$emit('confirm')" data-testid="confirm-ok">확인</button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({ message: String })
defineEmits(['confirm', 'cancel'])
</script>

<style scoped>
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.4); display: flex; align-items: center; justify-content: center; z-index: 300; }
.dialog { background: #fff; border-radius: 12px; padding: 24px; width: 90%; max-width: 360px; text-align: center; }
.message { font-size: 16px; margin-bottom: 20px; line-height: 1.5; }
.actions { display: flex; gap: 12px; }
.cancel-btn, .confirm-btn { flex: 1; padding: 12px; border: none; border-radius: 8px; font-size: 15px; cursor: pointer; min-height: 44px; }
.cancel-btn { background: #f5f5f5; color: #333; }
.confirm-btn { background: #1a237e; color: #fff; }
</style>
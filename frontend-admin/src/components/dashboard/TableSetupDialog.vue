<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import { useTableStore } from '@/stores/table'
import type { FormInstance } from 'element-plus'

const props = defineProps<{ visible: boolean }>()
const emit = defineEmits<{ (e: 'update:visible', val: boolean): void }>()
const { t } = useI18n()
const authStore = useAuthStore()
const tableStore = useTableStore()

const formRef = ref<FormInstance>()
const loading = ref(false)
const form = reactive({ tableNumber: 1, password: '' })

const rules = {
  tableNumber: [{ required: true, message: 'Required', trigger: 'blur' }],
  password: [{ required: true, message: 'Required', trigger: 'blur' }],
}

async function handleSubmit(): Promise<void> {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid || !authStore.storeId) return

  loading.value = true
  try {
    await tableStore.setupTable(authStore.storeId, form.tableNumber, form.password)
    ElMessage.success(t('table.setupSuccess'))
    emit('update:visible', false)
    form.tableNumber = 1
    form.password = ''
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <el-dialog
    :model-value="visible"
    :title="t('table.setup')"
    width="400px"
    data-testid="table-setup-dialog"
    @update:model-value="emit('update:visible', $event)"
  >
    <el-form ref="formRef" :model="form" :rules="rules" label-position="top">
      <el-form-item :label="t('table.tableNumber')" prop="tableNumber">
        <el-input-number v-model="form.tableNumber" :min="1" data-testid="input-table-number" />
      </el-form-item>
      <el-form-item :label="t('table.tablePassword')" prop="password">
        <el-input v-model="form.password" type="password" show-password data-testid="input-table-password" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="emit('update:visible', false)">{{ t('common.cancel') }}</el-button>
      <el-button type="primary" :loading="loading" data-testid="table-setup-submit" @click="handleSubmit">
        {{ t('common.confirm') }}
      </el-button>
    </template>
  </el-dialog>
</template>

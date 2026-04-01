<script setup lang="ts">
import { reactive, ref, watch, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import { useUserStore } from '@/stores/user'
import { UserRole } from '@/types/auth'
import type { User } from '@/types/user'
import type { FormInstance } from 'element-plus'

const props = defineProps<{
  visible: boolean
  user: User | null
}>()

const emit = defineEmits<{ (e: 'update:visible', val: boolean): void }>()
const { t } = useI18n()
const authStore = useAuthStore()
const userStore = useUserStore()

const formRef = ref<FormInstance>()
const loading = ref(false)
const isEdit = computed(() => !!props.user)

const form = reactive({
  username: '',
  password: '',
  role: UserRole.MANAGER as UserRole,
})

const rules = computed(() => ({
  username: [
    { required: true, message: () => t('user.validation.usernameRequired'), trigger: 'blur' },
    { min: 3, message: () => t('user.validation.usernameMinLength'), trigger: 'blur' },
    { max: 20, message: () => t('user.validation.usernameMaxLength'), trigger: 'blur' },
  ],
  password: isEdit.value
    ? [{ min: 6, message: () => t('user.validation.passwordMinLength'), trigger: 'blur' }]
    : [
        { required: true, message: () => t('user.validation.passwordRequired'), trigger: 'blur' },
        { min: 6, message: () => t('user.validation.passwordMinLength'), trigger: 'blur' },
      ],
  role: [{ required: true, message: () => t('user.validation.roleRequired'), trigger: 'change' }],
}))

watch(() => props.visible, (val) => {
  if (val && props.user) {
    form.username = props.user.username
    form.password = ''
    form.role = props.user.role as UserRole
  } else if (val) {
    form.username = ''
    form.password = ''
    form.role = UserRole.MANAGER
  }
})

async function handleSubmit(): Promise<void> {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid || !authStore.storeId) return

  loading.value = true
  try {
    if (props.user) {
      const data: Record<string, unknown> = { username: form.username, role: form.role }
      if (form.password) data.password = form.password
      await userStore.updateUser(authStore.storeId, props.user.id, data as any)
      ElMessage.success(t('user.updateSuccess'))
    } else {
      await userStore.createUser(authStore.storeId, {
        username: form.username,
        password: form.password,
        role: form.role,
      })
      ElMessage.success(t('user.createSuccess'))
    }
    emit('update:visible', false)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <el-dialog
    :model-value="visible"
    :title="user ? t('user.editUser') : t('user.addUser')"
    width="450px"
    data-testid="user-form-dialog"
    @update:model-value="emit('update:visible', $event)"
  >
    <el-form ref="formRef" :model="form" :rules="rules" label-position="top">
      <el-form-item :label="t('auth.username')" prop="username">
        <el-input v-model="form.username" data-testid="input-user-username" />
      </el-form-item>
      <el-form-item :label="t('auth.password')" prop="password">
        <el-input v-model="form.password" type="password" show-password :placeholder="isEdit ? '(optional)' : ''" data-testid="input-user-password" />
      </el-form-item>
      <el-form-item :label="t('user.role')" prop="role">
        <el-select v-model="form.role" data-testid="select-user-role">
          <el-option :label="t('auth.role.owner')" :value="UserRole.OWNER" />
          <el-option :label="t('auth.role.manager')" :value="UserRole.MANAGER" />
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="emit('update:visible', false)">{{ t('common.cancel') }}</el-button>
      <el-button type="primary" :loading="loading" data-testid="user-form-submit" @click="handleSubmit">
        {{ t('common.save') }}
      </el-button>
    </template>
  </el-dialog>
</template>

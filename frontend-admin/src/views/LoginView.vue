<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'
import type { LoginCredentials } from '@/types/auth'
import type { FormInstance } from 'element-plus'
import type { AxiosError } from 'axios'

const { t } = useI18n()
const router = useRouter()
const { login } = useAuth()

const formRef = ref<FormInstance>()
const loading = ref(false)
const errorMsg = ref('')

const form = reactive<LoginCredentials>({
  storeId: '',
  username: '',
  password: '',
})

const rules = {
  storeId: [{ required: true, message: () => t('auth.storeId'), trigger: 'blur' }],
  username: [{ required: true, message: () => t('auth.username'), trigger: 'blur' }],
  password: [{ required: true, message: () => t('auth.password'), trigger: 'blur' }],
}

async function handleLogin(): Promise<void> {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return

  loading.value = true
  errorMsg.value = ''
  try {
    await login(form)
    router.push('/')
  } catch (e: unknown) {
    const axiosError = e as AxiosError
    if (axiosError.response?.status === 429) {
      errorMsg.value = t('auth.rateLimited')
    } else {
      errorMsg.value = t('auth.loginFailed')
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div style="display: flex; justify-content: center; align-items: center; min-height: 100vh; background: #f5f7fa">
    <el-card style="width: 400px" data-testid="login-card">
      <template #header>
        <h2 style="text-align: center; margin: 0">{{ t('auth.login') }}</h2>
      </template>
      <el-form ref="formRef" :model="form" :rules="rules" label-position="top" @submit.prevent="handleLogin">
        <el-form-item :label="t('auth.storeId')" prop="storeId">
          <el-input v-model="form.storeId" data-testid="input-store-id" />
        </el-form-item>
        <el-form-item :label="t('auth.username')" prop="username">
          <el-input v-model="form.username" data-testid="input-username" />
        </el-form-item>
        <el-form-item :label="t('auth.password')" prop="password">
          <el-input v-model="form.password" type="password" show-password data-testid="input-password" />
        </el-form-item>
        <el-alert v-if="errorMsg" :title="errorMsg" type="error" show-icon :closable="false" style="margin-bottom: 16px" />
        <el-form-item>
          <el-button type="primary" :loading="loading" style="width: 100%" native-type="submit" data-testid="login-button">
            {{ t('auth.loginButton') }}
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

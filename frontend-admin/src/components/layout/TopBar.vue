<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { useAuth } from '@/composables/useAuth'
import { useRouter } from 'vue-router'
import SSEStatusIndicator from '@/components/common/SSEStatusIndicator.vue'
import LanguageSwitcher from '@/components/common/LanguageSwitcher.vue'

const emit = defineEmits<{ (e: 'toggleSidebar'): void }>()
const { t } = useI18n()
const { user, isOwner, logout } = useAuth()
const router = useRouter()

async function handleLogout(): Promise<void> {
  await logout()
  router.push('/login')
}
</script>

<template>
  <div style="display: flex; align-items: center; justify-content: space-between; height: 100%">
    <div style="display: flex; align-items: center; gap: 12px">
      <el-button text @click="emit('toggleSidebar')" data-testid="toggle-sidebar">
        <el-icon><i class="el-icon-s-fold" /></el-icon>☰
      </el-button>
      <span style="font-weight: 600">{{ user?.storeName }}</span>
    </div>
    <div style="display: flex; align-items: center; gap: 16px">
      <SSEStatusIndicator />
      <LanguageSwitcher />
      <span>{{ user?.username }}</span>
      <el-tag :type="isOwner ? 'danger' : 'info'" size="small">
        {{ isOwner ? t('auth.role.owner') : t('auth.role.manager') }}
      </el-tag>
      <el-button type="danger" text @click="handleLogout" data-testid="logout-button">
        {{ t('auth.logout') }}
      </el-button>
    </div>
  </div>
</template>

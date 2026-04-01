<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { useRoute } from 'vue-router'
import { usePermission } from '@/composables/usePermission'
import { Odometer, Dish, User } from '@element-plus/icons-vue'

defineProps<{ collapsed: boolean }>()

const { t } = useI18n()
const route = useRoute()
const { canManageMenu, canManageUser } = usePermission()
</script>

<template>
  <el-menu
    :default-active="route.path"
    :collapse="collapsed"
    router
    style="height: 100%; border-right: none"
    data-testid="sidebar-menu"
  >
    <el-menu-item index="/" data-testid="nav-dashboard">
      <el-icon><Odometer /></el-icon>
      <template #title>{{ t('nav.dashboard') }}</template>
    </el-menu-item>
    <el-menu-item v-if="canManageMenu" index="/menus" data-testid="nav-menus">
      <el-icon><Dish /></el-icon>
      <template #title>{{ t('nav.menuManage') }}</template>
    </el-menu-item>
    <el-menu-item v-if="canManageUser" index="/users" data-testid="nav-users">
      <el-icon><User /></el-icon>
      <template #title>{{ t('nav.userManage') }}</template>
    </el-menu-item>
  </el-menu>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { locale } = useI18n()

function changeLocale(lang: string): void {
  locale.value = lang
  localStorage.setItem('locale', lang)
}
</script>

<template>
  <el-dropdown trigger="click" data-testid="language-switcher" @command="changeLocale">
    <span style="cursor: pointer; font-size: 14px">{{ locale === 'ko' ? '한국어' : 'English' }}</span>
    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item command="ko" data-testid="lang-ko">한국어</el-dropdown-item>
        <el-dropdown-item command="en" data-testid="lang-en">English</el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>

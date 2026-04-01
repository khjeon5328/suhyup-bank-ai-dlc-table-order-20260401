<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import SideBar from './SideBar.vue'
import TopBar from './TopBar.vue'

const isCollapsed = ref(false)

function toggleSidebar(): void {
  isCollapsed.value = !isCollapsed.value
}

function handleResize(): void {
  isCollapsed.value = window.innerWidth < 1024
}

onMounted(() => {
  handleResize()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<template>
  <el-container class="app-layout" style="height: 100vh">
    <el-aside :width="isCollapsed ? '64px' : '200px'" style="transition: width 0.3s">
      <SideBar :collapsed="isCollapsed" />
    </el-aside>
    <el-container>
      <el-header>
        <TopBar @toggle-sidebar="toggleSidebar" />
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<style scoped>
.app-layout {
  overflow: hidden;
}
</style>

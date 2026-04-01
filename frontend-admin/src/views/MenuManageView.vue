<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import { useMenuStore } from '@/stores/menu'
import { useConfirm } from '@/composables/useConfirm'
import CategoryManageSection from '@/components/menu/CategoryManageSection.vue'
import MenuFormDialog from '@/components/menu/MenuFormDialog.vue'
import type { Menu } from '@/types/menu'

const { t } = useI18n()
const authStore = useAuthStore()
const menuStore = useMenuStore()
const { confirm } = useConfirm()

const showCategoryManage = ref(false)
const showMenuForm = ref(false)
const editingMenu = ref<Menu | null>(null)

const filteredMenus = computed(() => {
  if (!menuStore.selectedCategory) return menuStore.menus
  return menuStore.menus.filter((m) => m.category === menuStore.selectedCategory)
})

function handleAddMenu(): void {
  editingMenu.value = null
  showMenuForm.value = true
}

function handleEditMenu(menu: Menu): void {
  editingMenu.value = menu
  showMenuForm.value = true
}

async function handleDeleteMenu(menuId: number): Promise<void> {
  const confirmed = await confirm(t('menu.deleteConfirm'))
  if (!confirmed || !authStore.storeId) return
  await menuStore.deleteMenu(authStore.storeId, menuId)
  ElMessage.success(t('menu.deleteSuccess'))
}

onMounted(async () => {
  if (authStore.storeId) {
    await menuStore.fetchCategories(authStore.storeId)
    await menuStore.fetchMenus(authStore.storeId)
  }
})
</script>

<template>
  <div>
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px">
      <h2 style="margin: 0">{{ t('menu.title') }}</h2>
      <div style="display: flex; gap: 8px">
        <el-button data-testid="toggle-category-manage" @click="showCategoryManage = !showCategoryManage">
          {{ t('menu.categoryManage') }}
        </el-button>
        <el-button type="primary" data-testid="add-menu-button" @click="handleAddMenu">
          {{ t('menu.addMenu') }}
        </el-button>
      </div>
    </div>

    <CategoryManageSection v-if="showCategoryManage" style="margin-bottom: 20px" />

    <el-tabs v-model="menuStore.selectedCategory" data-testid="category-tabs">
      <el-tab-pane :label="t('dashboard.filterAll')" :name="null as any" />
      <el-tab-pane
        v-for="cat in menuStore.categories"
        :key="cat.id"
        :label="cat.name"
        :name="cat.name"
      />
    </el-tabs>

    <el-table :data="filteredMenus" v-loading="menuStore.loading" data-testid="menu-table">
      <el-table-column prop="name" :label="t('menu.name')" />
      <el-table-column prop="price" :label="t('menu.price')">
        <template #default="{ row }">{{ row.price.toLocaleString() }}</template>
      </el-table-column>
      <el-table-column prop="category" :label="t('menu.category')" />
      <el-table-column prop="displayOrder" :label="t('menu.displayOrder')" width="100" />
      <el-table-column :label="t('common.edit')" width="160">
        <template #default="{ row }">
          <el-button size="small" data-testid="edit-menu-button" @click="handleEditMenu(row)">
            {{ t('common.edit') }}
          </el-button>
          <el-button size="small" type="danger" data-testid="delete-menu-button" @click="handleDeleteMenu(row.id)">
            {{ t('common.delete') }}
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <MenuFormDialog
      :visible="showMenuForm"
      :menu="editingMenu"
      :categories="menuStore.categories"
      @update:visible="showMenuForm = $event"
    />
  </div>
</template>

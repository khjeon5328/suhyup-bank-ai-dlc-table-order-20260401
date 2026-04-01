<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/authStore'
import { useMenuStore } from '@/stores/menu'
import { useConfirm } from '@/composables/useConfirm'
import type { Category } from '@/types/menu'
import type { FormInstance } from 'element-plus'

const { t } = useI18n()
const authStore = useAuthStore()
const menuStore = useMenuStore()
const { confirm } = useConfirm()

const showForm = ref(false)
const editingCategory = ref<Category | null>(null)
const formRef = ref<FormInstance>()
const form = ref({ name: '' })

function handleAdd(): void {
  editingCategory.value = null
  form.value = { name: '' }
  showForm.value = true
}

function handleEdit(category: Category): void {
  editingCategory.value = category
  form.value = { name: category.name }
  showForm.value = true
}

async function handleDelete(category: Category): Promise<void> {
  if (category.menuCount > 0) {
    ElMessage.warning(t('menu.categoryHasMenus'))
    return
  }
  const confirmed = await confirm(t('menu.categoryDeleteConfirm'))
  if (!confirmed || !authStore.storeId) return
  await menuStore.deleteCategory(authStore.storeId, category.id)
}

async function handleSubmit(): Promise<void> {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid || !authStore.storeId) return

  if (editingCategory.value) {
    await menuStore.updateCategory(authStore.storeId, editingCategory.value.id, { name: form.value.name })
  } else {
    await menuStore.createCategory(authStore.storeId, { name: form.value.name })
  }
  showForm.value = false
}
</script>

<template>
  <el-card data-testid="category-manage-section">
    <template #header>
      <div style="display: flex; justify-content: space-between; align-items: center">
        <span>{{ t('menu.categoryManage') }}</span>
        <el-button size="small" type="primary" data-testid="add-category-button" @click="handleAdd">
          {{ t('menu.addCategory') }}
        </el-button>
      </div>
    </template>

    <el-table :data="menuStore.categories" size="small" data-testid="category-table">
      <el-table-column prop="name" :label="t('menu.categoryName')" />
      <el-table-column prop="menuCount" label="Menus" width="80" />
      <el-table-column prop="displayOrder" :label="t('menu.displayOrder')" width="100" />
      <el-table-column :label="t('common.edit')" width="160">
        <template #default="{ row }">
          <el-button size="small" data-testid="edit-category-button" @click="handleEdit(row)">
            {{ t('common.edit') }}
          </el-button>
          <el-button size="small" type="danger" data-testid="delete-category-button" @click="handleDelete(row)">
            {{ t('common.delete') }}
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="showForm" :title="editingCategory ? t('menu.editCategory') : t('menu.addCategory')" width="400px" append-to-body>
      <el-form ref="formRef" :model="form" label-position="top">
        <el-form-item :label="t('menu.categoryName')" prop="name" :rules="[{ required: true, message: t('menu.validation.nameRequired') }]">
          <el-input v-model="form.name" data-testid="input-category-name" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showForm = false">{{ t('common.cancel') }}</el-button>
        <el-button type="primary" data-testid="category-form-submit" @click="handleSubmit">{{ t('common.save') }}</el-button>
      </template>
    </el-dialog>
  </el-card>
</template>

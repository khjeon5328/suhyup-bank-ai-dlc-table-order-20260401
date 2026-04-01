<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import { useUserStore } from '@/stores/user'
import { useConfirm } from '@/composables/useConfirm'
import UserFormDialog from '@/components/user/UserFormDialog.vue'
import type { User } from '@/types/user'

const { t } = useI18n()
const authStore = useAuthStore()
const userStore = useUserStore()
const { confirm } = useConfirm()

const showUserForm = ref(false)
const editingUser = ref<User | null>(null)

function handleAddUser(): void {
  editingUser.value = null
  showUserForm.value = true
}

function handleEditUser(user: User): void {
  editingUser.value = user
  showUserForm.value = true
}

async function handleDeleteUser(userId: number): Promise<void> {
  if (userId === authStore.user?.id) {
    ElMessage.warning(t('user.cannotDeleteSelf'))
    return
  }
  const confirmed = await confirm(t('user.deleteConfirm'))
  if (!confirmed || !authStore.storeId) return
  await userStore.deleteUser(authStore.storeId, userId)
  ElMessage.success(t('user.deleteSuccess'))
}

onMounted(async () => {
  if (authStore.storeId) {
    await userStore.fetchUsers(authStore.storeId)
  }
})
</script>

<template>
  <div>
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px">
      <h2 style="margin: 0">{{ t('user.title') }}</h2>
      <el-button type="primary" data-testid="add-user-button" @click="handleAddUser">
        {{ t('user.addUser') }}
      </el-button>
    </div>

    <el-table :data="userStore.users" v-loading="userStore.loading" data-testid="user-table">
      <el-table-column prop="username" :label="t('auth.username')" />
      <el-table-column prop="role" :label="t('user.role')">
        <template #default="{ row }">
          <el-tag :type="row.role === 'owner' ? 'danger' : 'info'" size="small">
            {{ row.role === 'owner' ? t('auth.role.owner') : t('auth.role.manager') }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="createdAt" :label="t('user.createdAt')" />
      <el-table-column :label="t('common.edit')" width="160">
        <template #default="{ row }">
          <el-button size="small" data-testid="edit-user-button" @click="handleEditUser(row)">
            {{ t('common.edit') }}
          </el-button>
          <el-button size="small" type="danger" data-testid="delete-user-button" @click="handleDeleteUser(row.id)">
            {{ t('common.delete') }}
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <UserFormDialog
      :visible="showUserForm"
      :user="editingUser"
      @update:visible="showUserForm = $event"
    />
  </div>
</template>

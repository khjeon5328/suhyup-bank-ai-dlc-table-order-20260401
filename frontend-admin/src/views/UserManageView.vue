<template>
  <div class="user-manage">
    <div class="page-header">
      <h1>계정 관리</h1>
      <button class="add-btn" @click="openForm(null)" data-testid="user-add-btn">+ 계정 추가</button>
    </div>
    <div v-if="loading" class="loading">불러오는 중...</div>
    <table v-else class="data-table" data-testid="user-table">
      <thead><tr><th>사용자명</th><th>역할</th><th>관리</th></tr></thead>
      <tbody>
        <tr v-for="u in users" :key="u.id" :data-testid="`user-row-${u.id}`">
          <td>{{ u.username }}</td>
          <td>{{ u.role === 'owner' ? '점주' : '매니저' }}</td>
          <td>
            <button class="edit-btn" @click="openForm(u)" :data-testid="`user-edit-${u.id}`">수정</button>
            <button class="del-btn" @click="handleDelete(u)" :data-testid="`user-del-${u.id}`">삭제</button>
          </td>
        </tr>
      </tbody>
    </table>
    <UserForm v-if="showForm" :user="editingUser" :storeCode="auth.storeCode"
              @close="showForm = false" @saved="loadUsers" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import { userService } from '@/services/userService'
import UserForm from '@/components/UserForm.vue'
const auth = useAuthStore()
const users = ref([]); const loading = ref(false); const showForm = ref(false); const editingUser = ref(null)

function openForm(user) { editingUser.value = user; showForm.value = true }

async function loadUsers() {
  loading.value = true; showForm.value = false
  try { users.value = await userService.getUsers(auth.storeCode) } finally { loading.value = false }
}

async function handleDelete(u) {
  if (!confirm(`"${u.username}" 계정을 삭제하시겠습니까?`)) return
  try { await userService.deleteUser(auth.storeCode, u.id); await loadUsers() }
  catch (e) { alert(e.response?.data?.detail || '삭제에 실패했습니다.') }
}

onMounted(loadUsers)
</script>

<style scoped>
.user-manage h1 { font-size: 22px; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.add-btn { padding: 10px 20px; background: #1a237e; color: #fff; border: none; border-radius: 8px; cursor: pointer; min-height: 44px; }
.loading { text-align: center; padding: 40px; color: #999; }
.data-table { width: 100%; border-collapse: collapse; background: #fff; border-radius: 8px; overflow: hidden; }
.data-table th, .data-table td { padding: 12px 16px; text-align: left; border-bottom: 1px solid #f0f0f0; font-size: 14px; }
.data-table th { background: #f5f5f5; font-weight: 600; }
.edit-btn, .del-btn { padding: 6px 12px; border: none; border-radius: 6px; font-size: 12px; cursor: pointer; margin-right: 4px; min-height: 32px; }
.edit-btn { background: #e3f2fd; color: #1565c0; }
.del-btn { background: #ffebee; color: #c62828; }
</style>
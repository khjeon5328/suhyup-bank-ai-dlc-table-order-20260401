<template>
  <div class="menu-manage">
    <div class="page-header">
      <h1>메뉴 관리</h1>
      <button class="add-btn" @click="openForm(null)" data-testid="menu-add-btn">+ 메뉴 추가</button>
    </div>
    <div v-if="loading" class="loading">불러오는 중...</div>
    <table v-else class="menu-table" data-testid="menu-table">
      <thead><tr><th>순서</th><th>메뉴명</th><th>카테고리</th><th>가격</th><th>상태</th><th>관리</th></tr></thead>
      <tbody>
        <tr v-for="menu in menus" :key="menu.id" :data-testid="`menu-row-${menu.id}`">
          <td>{{ menu.sort_order }}</td>
          <td>{{ menu.name }}</td>
          <td>{{ getCategoryName(menu.category_id) }}</td>
          <td>{{ menu.price.toLocaleString() }}원</td>
          <td>{{ menu.is_active ? '판매중' : '숨김' }}</td>
          <td>
            <button class="edit-btn" @click="openForm(menu)" :data-testid="`menu-edit-${menu.id}`">수정</button>
            <button class="del-btn" @click="handleDelete(menu)" :data-testid="`menu-del-${menu.id}`">삭제</button>
          </td>
        </tr>
      </tbody>
    </table>
    <MenuForm v-if="showForm" :menu="editingMenu" :categories="categories" :storeId="auth.storeId"
              @close="showForm = false" @saved="loadData" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/authStore'
import { menuService } from '../services/menuService'
import MenuForm from '../components/MenuForm.vue'
const auth = useAuthStore()
const menus = ref([]); const categories = ref([]); const loading = ref(false)
const showForm = ref(false); const editingMenu = ref(null)

function getCategoryName(id) { return categories.value.find(c => c.id === id)?.name || '-' }
function openForm(menu) { editingMenu.value = menu; showForm.value = true }

async function loadData() {
  loading.value = true; showForm.value = false
  try {
    const [m, c] = await Promise.all([menuService.getMenus(auth.storeId), menuService.getCategories(auth.storeId)])
    menus.value = m; categories.value = c
  } finally { loading.value = false }
}

async function handleDelete(menu) {
  if (!confirm(`"${menu.name}" 메뉴를 삭제하시겠습니까?`)) return
  try { await menuService.deleteMenu(auth.storeId, menu.id); await loadData() }
  catch (e) { alert(e.response?.data?.detail || '삭제에 실패했습니다.') }
}

onMounted(loadData)
</script>

<style scoped>
.menu-manage h1 { font-size: 22px; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.add-btn { padding: 10px 20px; background: #1a237e; color: #fff; border: none; border-radius: 8px; cursor: pointer; min-height: 44px; }
.loading { text-align: center; padding: 40px; color: #999; }
.menu-table { width: 100%; border-collapse: collapse; background: #fff; border-radius: 8px; overflow: hidden; }
.menu-table th, .menu-table td { padding: 12px 16px; text-align: left; border-bottom: 1px solid #f0f0f0; font-size: 14px; }
.menu-table th { background: #f5f5f5; font-weight: 600; }
.edit-btn, .del-btn { padding: 6px 12px; border: none; border-radius: 6px; font-size: 12px; cursor: pointer; margin-right: 4px; min-height: 32px; }
.edit-btn { background: #e3f2fd; color: #1565c0; }
.del-btn { background: #ffebee; color: #c62828; }
</style>
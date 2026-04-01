<template>
  <div class="menu-page">
    <CategoryTabs :categories="categories" :activeId="activeCategory" @select="onCategorySelect" />
    <div v-if="isLoading" class="loading">메뉴를 불러오는 중...</div>
    <div v-else-if="errorMsg" class="error-msg" data-testid="menu-error">{{ errorMsg }}</div>
    <div v-else class="menu-grid" data-testid="menu-grid">
      <MenuCard v-for="menu in filteredMenus" :key="menu.id" :menu="menu"
                @click="openDetail(menu)" @add-to-cart="addToCart(menu)" />
    </div>
    <MenuDetailModal v-if="selectedMenu" :menu="selectedMenu" :visible="showDetail"
                     @close="showDetail = false" @add-to-cart="addToCartAndClose" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/authStore'
import { useCartStore } from '../stores/cartStore'
import { useOrderStore } from '../stores/orderStore'
import { menuService } from '../services/menuService'
import CategoryTabs from '../components/CategoryTabs.vue'
import MenuCard from '../components/MenuCard.vue'
import MenuDetailModal from '../components/MenuDetailModal.vue'

const authStore = useAuthStore()
const cartStore = useCartStore()
const orderStore = useOrderStore()

const categories = ref([])
const menus = ref([])
const activeCategory = ref(null)
const isLoading = ref(false)
const selectedMenu = ref(null)
const showDetail = ref(false)
const errorMsg = ref('')

const filteredMenus = computed(() => {
  if (!activeCategory.value) return menus.value
  return menus.value.filter(m => m.category_id === activeCategory.value)
})

function onCategorySelect(categoryId) {
  activeCategory.value = categoryId === activeCategory.value ? null : categoryId
}

function openDetail(menu) { selectedMenu.value = menu; showDetail.value = true }
function addToCart(menu) { cartStore.addItem(menu) }
function addToCartAndClose(menu) { cartStore.addItem(menu); showDetail.value = false }

onMounted(async () => {
  isLoading.value = true
  try {
    const [cats, menuList] = await Promise.all([
      menuService.getCategories(authStore.storeCode),
      menuService.getMenus(authStore.storeCode)
    ])
    categories.value = cats
    menus.value = menuList
  } catch (err) {
    errorMsg.value = '메뉴를 불러오지 못했습니다. 새로고침해 주세요.'
  } finally {
    isLoading.value = false
  }
  orderStore.connectSSE()
})
</script>

<style scoped>
.menu-page { padding: 16px; }
.loading { text-align: center; padding: 40px; color: #999; }
.error-msg { text-align: center; padding: 40px; color: #f44336; }
.menu-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 12px; padding-top: 12px; }
</style>
<template>
  <div class="menu-page">
    <CategoryTabs :categories="categories" :activeId="activeCategory" @select="onCategorySelect" />
    <div v-if="isLoading" class="loading">메뉴를 불러오는 중...</div>
    <div v-else-if="errorMsg" class="error-msg" data-testid="menu-error">{{ errorMsg }}</div>
    <div v-else class="menu-grid" data-testid="menu-grid">
      <MenuCard v-for="menu in filteredMenus" :key="menu.id" :menu="menu"
                @click="openDetail(menu)" @add-to-cart="onAddToCart(menu)" />
    </div>
    <MenuDetailModal v-if="selectedMenu" :menu="selectedMenu" :visible="showDetail"
                     @close="showDetail = false" @add-to-cart="onAddToCartFromDetail" />

    <!-- 화면 중앙 장바구니 추가 오버레이 -->
    <Transition name="overlay">
      <div v-if="showOverlay" class="cart-overlay">
        <div class="cart-overlay-content">
          <div class="cart-icon-circle">
            <span class="cart-icon">🛒</span>
            <span class="check-icon">✓</span>
          </div>
          <p class="overlay-text">장바구니에 담았어요</p>
        </div>
      </div>
    </Transition>
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
const showOverlay = ref(false)
let overlayTimer = null

const filteredMenus = computed(() => {
  if (!activeCategory.value) return menus.value
  return menus.value.filter(m => m.category_id === activeCategory.value)
})

function onCategorySelect(categoryId) {
  activeCategory.value = categoryId === activeCategory.value ? null : categoryId
}

function openDetail(menu) { selectedMenu.value = menu; showDetail.value = true }

function playAddSound() {
  try {
    const ctx = new (window.AudioContext || window.webkitAudioContext)()
    // 두 음을 빠르게 연속 재생 (띵동)
    const play = (freq, start, dur) => {
      const osc = ctx.createOscillator()
      const gain = ctx.createGain()
      osc.connect(gain); gain.connect(ctx.destination)
      osc.type = 'sine'
      osc.frequency.value = freq
      gain.gain.setValueAtTime(0.2, ctx.currentTime + start)
      gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + start + dur)
      osc.start(ctx.currentTime + start)
      osc.stop(ctx.currentTime + start + dur)
    }
    play(880, 0, 0.15)
    play(1320, 0.12, 0.2)
  } catch (e) { /* ignore */ }
}

function showCartEffect() {
  if (overlayTimer) clearTimeout(overlayTimer)
  showOverlay.value = true
  overlayTimer = setTimeout(() => { showOverlay.value = false }, 1000)
}

function onAddToCart(menu) {
  cartStore.addItem(menu)
  playAddSound()
  showCartEffect()
}

function onAddToCartFromDetail(menu) {
  cartStore.addItem(menu)
  playAddSound()
  showDetail.value = false
  showCartEffect()
}

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

/* 중앙 오버레이 */
.cart-overlay {
  position: fixed; inset: 0;
  display: flex; align-items: center; justify-content: center;
  z-index: 9999; pointer-events: none;
}
.cart-overlay-content {
  display: flex; flex-direction: column; align-items: center;
  background: rgba(0,0,0,0.75); border-radius: 20px;
  padding: 28px 40px; gap: 12px;
}
.cart-icon-circle {
  width: 72px; height: 72px; border-radius: 50%;
  background: #4caf50; display: flex; align-items: center; justify-content: center;
  position: relative;
}
.cart-icon { font-size: 32px; }
.check-icon {
  position: absolute; bottom: -2px; right: -2px;
  background: #fff; color: #4caf50; font-size: 18px; font-weight: 900;
  width: 24px; height: 24px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 1px 3px rgba(0,0,0,0.3);
}
.overlay-text { color: #fff; font-size: 16px; font-weight: 600; }

/* 오버레이 트랜지션 */
.overlay-enter-active { animation: overlayIn 0.25s ease-out; }
.overlay-leave-active { animation: overlayOut 0.3s ease-in; }
@keyframes overlayIn { from { opacity: 0; transform: scale(0.7); } to { opacity: 1; transform: scale(1); } }
@keyframes overlayOut { from { opacity: 1; transform: scale(1); } to { opacity: 0; transform: scale(0.8); } }
</style>

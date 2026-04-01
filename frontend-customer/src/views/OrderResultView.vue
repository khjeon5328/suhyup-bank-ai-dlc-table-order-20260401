<template>
  <div class="result-page" data-testid="order-result">
    <div class="result-card">
      <div class="success-icon">✅</div>
      <h1>주문 완료</h1>
      <p class="order-no" data-testid="result-order-no">주문번호: {{ orderId }}</p>
      <p class="redirect-msg">{{ countdown }}초 후 메뉴 화면으로 이동합니다</p>
      <router-link to="/" class="go-menu-btn" data-testid="result-go-menu">메뉴로 바로가기</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({ orderId: String })
const router = useRouter()
const countdown = ref(5)
let timer = null

onMounted(() => {
  timer = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(timer)
      router.push('/')
    }
  }, 1000)
})

onUnmounted(() => { if (timer) clearInterval(timer) })
</script>

<style scoped>
.result-page { display: flex; align-items: center; justify-content: center; min-height: 80vh; padding: 24px; }
.result-card { background: #fff; border-radius: 16px; padding: 40px; text-align: center; width: 100%; max-width: 400px; }
.success-icon { font-size: 64px; margin-bottom: 16px; }
h1 { font-size: 24px; margin-bottom: 12px; }
.order-no { font-size: 18px; color: #1976d2; font-weight: 600; margin-bottom: 16px; }
.redirect-msg { color: #999; margin-bottom: 24px; }
.go-menu-btn { display: inline-block; padding: 14px 32px; background: #1976d2; color: #fff; border-radius: 8px; text-decoration: none; font-size: 16px; min-height: 48px; }
</style>
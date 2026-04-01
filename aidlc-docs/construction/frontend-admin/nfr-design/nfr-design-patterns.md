# Unit 4: frontend-admin - NFR Design Patterns

> 담당자: 수민

---

## 1. 성능 패턴 (Performance)

### PATTERN-PERF-01: Route-based Code Splitting

라우트 단위 lazy import로 초기 로딩 최소화.

```typescript
// router/index.ts
const routes = [
  { path: '/login', component: () => import('@/views/LoginView.vue') },
  { path: '/', component: () => import('@/views/DashboardView.vue') },
  { path: '/menus', component: () => import('@/views/MenuManageView.vue') },
  { path: '/users', component: () => import('@/views/UserManageView.vue') },
]
```

- 각 뷰가 별도 청크로 분리되어 필요 시점에 로드
- 초기 번들 크기 감소 → 첫 로딩 속도 개선

---

### PATTERN-PERF-02: Element Plus Auto-Import

unplugin을 사용하여 Element Plus 컴포넌트를 자동 import, 트리쉐이킹 적용.

```typescript
// vite.config.ts
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'

export default defineConfig({
  plugins: [
    AutoImport({ resolvers: [ElementPlusResolver()] }),
    Components({ resolvers: [ElementPlusResolver()] }),
  ],
})
```

- 사용하는 컴포넌트만 번들에 포함
- 전체 Element Plus import 대비 ~60% 번들 크기 절감

---

### PATTERN-PERF-03: Vite Manual Chunks

벤더 라이브러리를 논리적 그룹으로 분리하여 캐싱 효율 극대화.

```typescript
// vite.config.ts
build: {
  rollupOptions: {
    output: {
      manualChunks: {
        'vendor-vue': ['vue', 'vue-router', 'pinia'],
        'vendor-element': ['element-plus'],
        'vendor-i18n': ['vue-i18n'],
        'vendor-utils': ['axios', 'dayjs', 'vuedraggable'],
      }
    }
  }
}
```

| 청크 | 포함 라이브러리 | 예상 크기 (gzip) |
|------|---------------|-----------------|
| vendor-vue | vue, vue-router, pinia | ~45KB |
| vendor-element | element-plus (auto-import) | ~120KB |
| vendor-i18n | vue-i18n | ~15KB |
| vendor-utils | axios, dayjs, vuedraggable | ~25KB |

---

### PATTERN-PERF-04: Pinia storeToRefs 최적화

`storeToRefs`로 반응성 유지하면서 불필요한 리렌더링 방지.

```typescript
// 컴포넌트에서 사용
import { storeToRefs } from 'pinia'
import { useOrderStore } from '@/stores/orderStore'

const orderStore = useOrderStore()
const { ordersByTable, isLoading } = storeToRefs(orderStore)
// 액션은 직접 구조분해
const { fetchOrders, updateOrderStatus } = orderStore
```

- `storeToRefs`: state/getters만 반응형 ref로 변환
- 액션은 반응형 래핑 불필요 → 직접 구조분해

---

## 2. 보안 패턴 (Security)

### PATTERN-SEC-01: Access/Refresh Token Flow

```
[로그인 요청]
  → POST /auth/login { store_identifier, username, password }
  → 응답: { access_token } + Set-Cookie: refresh_token (httpOnly, Secure)

[Access Token 저장]
  → Pinia authStore 메모리에만 저장 (XSS 방어)
  → localStorage/sessionStorage 사용 금지

[Refresh Token 저장]
  → httpOnly Cookie (JavaScript 접근 불가)
  → Secure 플래그 (HTTPS만 전송)
  → SameSite=Strict

[토큰 갱신 플로우]
  → API 요청 → 401 응답
  → POST /auth/refresh (Cookie 자동 전송)
  → 새 access_token 발급 → 원래 요청 재시도

[로그아웃]
  → POST /auth/logout
  → Pinia accessToken 초기화
  → 서버에서 refresh_token Cookie 삭제
```

---

### PATTERN-SEC-02: Axios Security Interceptor (401 큐 패턴)

동시 다발적 401 응답 시 토큰 갱신 요청을 1회로 제한.

```typescript
let isRefreshing = false
let failedQueue: Array<{ resolve: Function; reject: Function }> = []

const processQueue = (error: any, token: string | null) => {
  failedQueue.forEach(({ resolve, reject }) => {
    error ? reject(error) : resolve(token)
  })
  failedQueue = []
}

// 응답 인터셉터
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        // 갱신 중이면 큐에 추가하고 대기
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject })
        }).then((token) => {
          originalRequest.headers.Authorization = `Bearer ${token}`
          return apiClient(originalRequest)
        })
      }
      originalRequest._retry = true
      isRefreshing = true
      try {
        const { access_token } = await authApi.refresh()
        authStore.setAccessToken(access_token)
        processQueue(null, access_token)
        originalRequest.headers.Authorization = `Bearer ${access_token}`
        return apiClient(originalRequest)
      } catch (refreshError) {
        processQueue(refreshError, null)
        authStore.logout()
        router.push('/login')
        return Promise.reject(refreshError)
      } finally {
        isRefreshing = false
      }
    }
    return Promise.reject(error)
  }
)
```

---

### PATTERN-SEC-03: Input Sanitization Utility

XSS 방지를 위한 입력값 정제 유틸리티.

```typescript
// utils/sanitize.ts
export function sanitizeInput(input: string): string {
  return input
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;')
}

export function sanitizeObject<T extends Record<string, any>>(obj: T): T {
  const sanitized = { ...obj }
  for (const key in sanitized) {
    if (typeof sanitized[key] === 'string') {
      sanitized[key] = sanitizeInput(sanitized[key]) as any
    }
  }
  return sanitized
}
```

---

## 3. 신뢰성 패턴 (Reliability)

### PATTERN-REL-01: Vue Global Error Handler

```typescript
// main.ts
app.config.errorHandler = (err, instance, info) => {
  console.error('[GlobalErrorHandler]', {
    error: err,
    component: instance?.$options?.name || 'Unknown',
    info,
    timestamp: new Date().toISOString(),
  })
  // 사용자에게 안전한 에러 메시지 표시
  ElMessage.error('예기치 않은 오류가 발생했습니다.')
}
```

---

### PATTERN-REL-02: SSE Reconnection

최대 3회 재시도, 즉시 재연결 시도.

```typescript
// sseService.ts
const MAX_RETRIES = 3
let retryCount = 0

function connect(storeId: number): EventSource {
  const es = new EventSource(`${SSE_BASE_URL}/stores/${storeId}/events`)

  es.onopen = () => { retryCount = 0 }

  es.onerror = () => {
    es.close()
    if (retryCount < MAX_RETRIES) {
      retryCount++
      connect(storeId)  // 즉시 재연결
    } else {
      // 연결 실패 상태 표시
      sseStore.setDisconnected()
    }
  }
  return es
}
```

- 최대 재시도: 3회
- 재연결 지연: 없음 (즉시)
- 실패 시: SSEStatusIndicator에 "연결 끊김" 표시

---

### PATTERN-REL-03: GET Request Auto-Retry

GET 요청에 한해 네트워크 에러 또는 5xx 응답 시 1회 자동 재시도.

```typescript
// apiClient.ts 요청 인터셉터
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const config = error.config
    if (
      config.method === 'get' &&
      !config._retried &&
      (isNetworkError(error) || is5xxError(error))
    ) {
      config._retried = true
      return apiClient(config)
    }
    return Promise.reject(error)
  }
)
```

- 대상: GET 요청만
- 재시도 횟수: 1회
- 조건: 네트워크 에러 또는 5xx 서버 에러

---

## 4. 상태 관리 패턴 (State Management)

### PATTERN-STATE-01: Store-based Loading/Error Pattern

모든 스토어에 일관된 loading/error 상태 관리.

```typescript
// stores/orderStore.ts
export const useOrderStore = defineStore('order', {
  state: () => ({
    orders: [] as Order[],
    isLoading: false,
    error: null as string | null,
  }),
  actions: {
    async fetchOrders(tableId: number) {
      this.isLoading = true
      this.error = null
      try {
        this.orders = await orderApi.getOrders(tableId)
      } catch (e: any) {
        this.error = e.message || '주문 목록을 불러올 수 없습니다.'
      } finally {
        this.isLoading = false
      }
    },
  },
})
```

---

### PATTERN-STATE-02: useAsyncAction Composable

반복되는 async 액션의 loading/error 패턴을 추상화.

```typescript
// composables/useAsyncAction.ts
export function useAsyncAction<T>(action: (...args: any[]) => Promise<T>) {
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const execute = async (...args: any[]): Promise<T | undefined> => {
    isLoading.value = true
    error.value = null
    try {
      const result = await action(...args)
      return result
    } catch (e: any) {
      error.value = e.message || '오류가 발생했습니다.'
      return undefined
    } finally {
      isLoading.value = false
    }
  }

  return { isLoading, error, execute }
}
```

---

## 5. 다국어 패턴 (i18n)

### PATTERN-I18N-01: vue-i18n Setup with localStorage Persistence

```typescript
// i18n/index.ts
import { createI18n } from 'vue-i18n'
import ko from '@/locales/ko.json'
import en from '@/locales/en.json'

const savedLocale = localStorage.getItem('locale') || 'ko'

export const i18n = createI18n({
  legacy: false,           // Composition API 모드
  locale: savedLocale,
  fallbackLocale: 'ko',
  messages: { ko, en },
})

// locale 변경 시 localStorage 동기화
export function setLocale(locale: 'ko' | 'en') {
  i18n.global.locale.value = locale
  localStorage.setItem('locale', locale)
}
```

---

### PATTERN-I18N-02: Language File Structure

```json
// locales/ko.json
{
  "common": { "save": "저장", "cancel": "취소", "delete": "삭제", "confirm": "확인", "search": "검색" },
  "auth": { "login": "로그인", "logout": "로그아웃", "storeId": "매장 식별자", "username": "사용자명", "password": "비밀번호" },
  "dashboard": { "title": "대시보드", "totalTables": "총 테이블", "activeSessions": "활성 세션", "pendingOrders": "대기 주문" },
  "order": { "pending": "대기중", "preparing": "준비중", "completed": "완료", "delete": "주문 삭제", "total": "총 주문액" },
  "menu": { "title": "메뉴 관리", "addMenu": "메뉴 추가", "editMenu": "메뉴 수정", "category": "카테고리" },
  "user": { "title": "사용자 관리", "addUser": "사용자 추가", "role": "역할" },
  "table": { "setup": "테이블 설정", "endSession": "이용 완료", "history": "과거 내역" },
  "sse": { "connected": "실시간 연결", "disconnected": "연결 끊김" }
}
```

```json
// locales/en.json
{
  "common": { "save": "Save", "cancel": "Cancel", "delete": "Delete", "confirm": "Confirm", "search": "Search" },
  "auth": { "login": "Login", "logout": "Logout", "storeId": "Store ID", "username": "Username", "password": "Password" },
  "dashboard": { "title": "Dashboard", "totalTables": "Total Tables", "activeSessions": "Active Sessions", "pendingOrders": "Pending Orders" },
  "order": { "pending": "Pending", "preparing": "Preparing", "completed": "Completed", "delete": "Delete Order", "total": "Total Amount" },
  "menu": { "title": "Menu Management", "addMenu": "Add Menu", "editMenu": "Edit Menu", "category": "Category" },
  "user": { "title": "User Management", "addUser": "Add User", "role": "Role" },
  "table": { "setup": "Table Setup", "endSession": "End Session", "history": "Order History" },
  "sse": { "connected": "Connected", "disconnected": "Disconnected" }
}
```

---

### PATTERN-I18N-03: Component Usage with useI18n

```vue
<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>

<template>
  <h1>{{ t('dashboard.title') }}</h1>
  <el-button>{{ t('common.save') }}</el-button>
</template>
```

---

## 6. 라우트 가드 패턴 (Route Guard)

### PATTERN-GUARD-01: Auth + Role-based Route Guard

```typescript
// router/index.ts
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  // 로그인 페이지 접근
  if (to.path === '/login') {
    return authStore.isAuthenticated ? next('/') : next()
  }

  // 미인증 → 로그인 페이지로
  if (!authStore.isAuthenticated) {
    return next('/login')
  }

  // 역할 기반 접근 제어
  const requiredRole = to.meta.requiredRole as string | undefined
  if (requiredRole && authStore.user?.role !== requiredRole) {
    return next('/')  // 권한 없음 → 대시보드로
  }

  next()
})
```

라우트 메타 설정:
```typescript
{
  path: '/menus',
  component: () => import('@/views/MenuManageView.vue'),
  meta: { requiresAuth: true, requiredRole: 'owner' }
}
```

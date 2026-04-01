# Unit 4: frontend-admin - Logical Components

> 담당자: 수민

---

## 아키텍처 개요

```
+--------------------------------------------------+
|                  Views (Pages)                    |
|  LoginView | DashboardView | MenuManageView |    |
|  UserManageView                                   |
+--------------------------------------------------+
|               Components (UI)                     |
|  Layout: AppLayout, Sidebar, TopBar               |
|  Common: OrderStatusBadge, OrderStatusButton,     |
|          SSEStatusIndicator, LanguageSwitcher      |
|  Dashboard: TableCard, OrderDetailModal,          |
|             TableSetupDialog, OrderHistoryPanel    |
|  Menu: CategoryManageSection, MenuFormDialog      |
|  User: UserFormDialog                             |
+--------------------------------------------------+
|            Composables (Logic)                    |
|  useAuth | useSSE | useAsyncAction |              |
|  usePermission | useConfirm | useImageUpload      |
+--------------------------------------------------+
|           Pinia Stores (State)                    |
|  authStore | orderStore | tableStore |            |
|  menuStore | userStore                            |
+--------------------------------------------------+
|          Services (API Layer)                     |
|  apiClient | authApi | orderApi | tableApi |      |
|  menuApi | userApi | imageApi | sseService        |
+--------------------------------------------------+
|              External                             |
|  Backend REST API | SSE Endpoint | S3 (Image)     |
+--------------------------------------------------+
```

데이터 흐름: Views → Components → Composables → Pinia Stores → Services → External

---

## Composables 정의

### useAuth
```typescript
interface UseAuth {
  // Provided
  authStore: AuthStore

  // Returns
  isAuthenticated: ComputedRef<boolean>
  user: ComputedRef<AuthUser | null>
  login: (credentials: LoginCredentials) => Promise<void>
  logout: () => Promise<void>
  checkAuth: () => Promise<boolean>
}
```
- 로그인/로그아웃 플로우 캡슐화
- 토큰 갱신 상태 관리
- 라우터 가드에서 사용

### useSSE
```typescript
interface UseSSE {
  // Provided
  storeId: number

  // Returns
  isConnected: Ref<boolean>
  connect: () => void
  disconnect: () => void
  onOrderCreated: (handler: (order: Order) => void) => void
  onOrderStatusChanged: (handler: (data: { order_id: number; status: OrderStatus }) => void) => void
  onOrderDeleted: (handler: (data: { order_id: number }) => void) => void
}
```
- SSE 연결/해제 관리
- 이벤트 타입별 핸들러 등록
- 자동 재연결 (최대 3회)

### useAsyncAction
```typescript
interface UseAsyncAction<T> {
  // Provided
  action: (...args: any[]) => Promise<T>

  // Returns
  isLoading: Ref<boolean>
  error: Ref<string | null>
  execute: (...args: any[]) => Promise<T | undefined>
}
```
- 비동기 액션의 loading/error 상태 자동 관리
- 컴포넌트에서 반복 코드 제거

### usePermission
```typescript
interface UsePermission {
  // Returns
  isOwner: ComputedRef<boolean>
  isManager: ComputedRef<boolean>
  canManageMenu: ComputedRef<boolean>
  canManageUser: ComputedRef<boolean>
  canDeleteOrder: ComputedRef<boolean>
  canSetupTable: ComputedRef<boolean>
}
```
- 역할 기반 권한 체크 로직 중앙화
- 컴포넌트에서 `v-if="canDeleteOrder"` 형태로 사용

### useConfirm
```typescript
interface UseConfirm {
  // Returns
  confirm: (message: string, title?: string) => Promise<boolean>
  confirmDelete: (itemName: string) => Promise<boolean>
}
```
- Element Plus `ElMessageBox.confirm` 래핑
- 삭제/이용완료 등 위험 액션 전 확인 다이얼로그

### useImageUpload
```typescript
interface UseImageUpload {
  // Returns
  imageUrl: Ref<string | null>
  isUploading: Ref<boolean>
  uploadImage: (file: File) => Promise<string>
  clearImage: () => void
}
```
- 이미지 업로드 → S3 URL 반환
- 업로드 진행 상태 관리
- 메뉴 폼에서 사용

---

## Services 레이어

### apiClient (Axios 인스턴스)

```
[요청 인터셉터]
  → Authorization: Bearer {accessToken} 헤더 추가
  → Content-Type 설정

[응답 인터셉터]
  → 성공 (2xx): response.data 반환
  → 401: 토큰 갱신 큐 패턴 (PATTERN-SEC-02)
  → 네트워크/5xx + GET: 1회 자동 재시도 (PATTERN-REL-03)
  → 기타 에러: Promise.reject
```

### sseService

```
[connect(storeId)]
  → new EventSource(SSE_BASE_URL/stores/{storeId}/events)
  → onopen: retryCount = 0
  → onmessage: 이벤트 타입별 핸들러 디스패치
  → onerror: 재연결 시도 (최대 3회)

[이벤트 처리]
  → order_created: orderStore에 주문 추가 + tableStore NEW 뱃지
  → order_status_changed: orderStore 상태 업데이트
  → order_deleted: orderStore에서 주문 제거
```

---

## Pinia Stores 상세 State

### authStore
```typescript
state: {
  accessToken: string | null       // 메모리만 (XSS 방어)
  user: AuthUser | null            // { id, store_id, username, role, store_name }
}
getters: {
  isAuthenticated: boolean         // !!accessToken && !!user
  isOwner: boolean                 // user?.role === 'owner'
  storeName: string                // user?.store_name || ''
}
```

### orderStore
```typescript
state: {
  ordersByTable: Map<number, Order[]>   // tableId → Order[]
  orderHistory: OrderHistory[]          // 과거 주문 내역
  isLoading: boolean
  error: string | null
}
getters: {
  getOrdersByTable: (tableId) => Order[]
  getPendingCount: number
  getTotalAmountByTable: (tableId) => number
}
```

### tableStore
```typescript
state: {
  tables: TableSummary[]               // 전체 테이블 목록
  newOrderTableIds: Set<number>         // NEW 뱃지 표시 대상
  isLoading: boolean
  error: string | null
}
getters: {
  activeTableCount: number
  getTableById: (id) => TableSummary | undefined
}
```

### menuStore
```typescript
state: {
  menus: Menu[]                         // 현재 카테고리의 메뉴 목록
  categories: Category[]               // 전체 카테고리 목록
  selectedCategoryId: number | null     // 선택된 카테고리
  isLoading: boolean
  error: string | null
}
getters: {
  filteredMenus: Menu[]                 // selectedCategoryId 기준 필터
  categoryOptions: { label, value }[]   // el-select용
}
```

### userStore
```typescript
state: {
  users: User[]                         // 매장 사용자 목록
  isLoading: boolean
  error: string | null
}
getters: {
  ownerCount: number
  managerCount: number
}
```

---

## 빌드 출력 구조

```
dist/
├── index.html
├── assets/
│   ├── index-[hash].js          # 앱 코드 (~30KB gzip)
│   ├── vendor-vue-[hash].js     # Vue 코어 (~45KB gzip)
│   ├── vendor-element-[hash].js # Element Plus (~120KB gzip)
│   ├── vendor-i18n-[hash].js    # vue-i18n (~15KB gzip)
│   ├── vendor-utils-[hash].js   # axios, dayjs 등 (~25KB gzip)
│   ├── LoginView-[hash].js      # Lazy chunk
│   ├── MenuManageView-[hash].js # Lazy chunk
│   ├── UserManageView-[hash].js # Lazy chunk
│   └── index-[hash].css         # 스타일
```

**예상 초기 로드 크기**: ~235KB (gzip)
- vendor-vue + vendor-element + vendor-i18n + vendor-utils + index = ~235KB
- 라우트별 lazy chunk는 네비게이션 시 추가 로드

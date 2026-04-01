# Code Generation Plan - Unit 4: frontend-admin

> 담당자: 수민

## Unit Context
- **유닛**: frontend-admin (관리자용 Vue.js SPA)
- **기술 스택**: Vue.js 3.4+ + TypeScript 5.x + Pinia + Vue Router + Element Plus + Vite
- **코드 위치**: `frontend-admin/`
- **스토리**: US-O01~O11, US-M01~M04 (15개)

---

## Story Mapping

| Step | 관련 스토리 | 설명 |
|------|-----------|------|
| Step 1 | 전체 | 프로젝트 초기화 및 설정 |
| Step 2 | 전체 | TypeScript 타입 정의 |
| Step 3 | 전체 | 다국어 리소스 |
| Step 4-5 | 전체 | API 서비스 레이어 + 테스트 |
| Step 6-7 | 전체 | Pinia 스토어 + 테스트 |
| Step 8-9 | 전체 | Composables + 테스트 |
| Step 10 | US-O01, US-M01 | 라우터 + 가드 |
| Step 11 | 전체 | 레이아웃 컴포넌트 |
| Step 12 | US-O02~O05, US-M02 | 공통 컴포넌트 |
| Step 13 | US-O01, US-M01 | 로그인 페이지 |
| Step 14 | US-O02, US-M02 | 대시보드 + 테이블 카드 |
| Step 15 | US-O03~O05 | 주문 상세 모달 |
| Step 16 | US-O06 | 테이블 설정 다이얼로그 |
| Step 17 | US-O07~O08, US-M03~M04 | 주문 이력 패널 |
| Step 18 | US-O09~O10 | 메뉴 관리 페이지 |
| Step 19 | US-O11 | 사용자 관리 페이지 |
| Step 20 | 전체 | 컴포넌트 테스트 |
| Step 21 | 전체 | 앱 엔트리 |
| Step 22 | 전체 | 요약 문서 |

---

## Generation Steps

### Step 1: 프로젝트 초기화 및 설정
- [x] package.json (의존성 정의)
- [x] vite.config.ts (Element Plus auto-import, manual chunks)
- [x] tsconfig.json (strict, ES2020, bundler moduleResolution)
- [x] .eslintrc.cjs (TypeScript + Vue 규칙)
- [x] .prettierrc
- [x] .husky/pre-commit (lint-staged 실행)
- [x] .env.example, .env.development

### Step 2: TypeScript 타입 정의
- [x] src/types/auth.ts (LoginCredentials, AuthTokens, AuthUser, UserRole)
- [x] src/types/order.ts (Order, OrderItem, OrderStatus, OrderHistory, OrderStatusCount)
- [x] src/types/table.ts (Table, TableSession, TableSummary)
- [x] src/types/menu.ts (Menu, MenuCreateRequest, MenuUpdateRequest, Category, CategoryCreateRequest)
- [x] src/types/user.ts (User, UserCreateRequest, UserUpdateRequest)
- [x] src/types/sse.ts (SSEEvent, SSEEventType)
- [x] src/types/api.ts (ApiResponse, ApiError, PaginatedResponse, DateRange)

### Step 3: 다국어 리소스 (i18n)
- [x] src/locales/ko.json
- [x] src/locales/en.json
- [x] src/i18n/index.ts (vue-i18n 설정, localStorage 연동)

### Step 4: API 서비스 레이어
- [x] src/services/apiClient.ts (Axios 인스턴스, 인터셉터, 401 큐 패턴)
- [x] src/services/authApi.ts (login, logout, refresh, getMe)
- [x] src/services/orderApi.ts (getOrders, updateStatus, deleteOrder)
- [x] src/services/tableApi.ts (getTables, setupTable, endSession, getHistory)
- [x] src/services/menuApi.ts (CRUD + 순서 변경)
- [x] src/services/userApi.ts (CRUD)
- [x] src/services/imageApi.ts (uploadImage)
- [x] src/services/sseService.ts (connect, disconnect, 이벤트 핸들링)

### Step 5: API 서비스 테스트
- [x] tests/services/apiClient.test.ts (인터셉터, 401 큐, 재시도)
- [x] tests/services/authApi.test.ts
- [x] tests/services/orderApi.test.ts
- [x] tests/services/sseService.test.ts

### Step 6: Pinia 스토어
- [x] src/stores/authStore.ts (accessToken 메모리 관리, user 상태)
- [x] src/stores/orderStore.ts (ordersByTable Map, SSE 이벤트 처리)
- [x] src/stores/tableStore.ts (tables, newOrderTableIds Set)
- [x] src/stores/menuStore.ts (menus, categories, selectedCategory)
- [x] src/stores/userStore.ts (users CRUD)

### Step 7: 스토어 테스트
- [x] tests/stores/authStore.test.ts
- [x] tests/stores/orderStore.test.ts
- [x] tests/stores/tableStore.test.ts
- [x] tests/stores/menuStore.test.ts
- [x] tests/stores/userStore.test.ts

### Step 8: Composables
- [x] src/composables/useAuth.ts
- [x] src/composables/useSSE.ts
- [x] src/composables/useAsyncAction.ts
- [x] src/composables/usePermission.ts
- [x] src/composables/useConfirm.ts
- [x] src/composables/useImageUpload.ts

### Step 9: Composable 테스트
- [x] tests/composables/useAsyncAction.test.ts
- [x] tests/composables/usePermission.test.ts

### Step 10: 라우터
- [x] src/router/index.ts (라우트 정의, 인증 + 역할 가드)

### Step 11: 레이아웃 컴포넌트
- [x] src/components/layout/AppLayout.vue
- [x] src/components/layout/Sidebar.vue (역할 기반 메뉴 렌더링)
- [x] src/components/layout/TopBar.vue (SSE 상태, 언어 전환, 사용자 정보)

### Step 12: 공통 컴포넌트
- [x] src/components/common/OrderStatusBadge.vue
- [x] src/components/common/OrderStatusButton.vue
- [x] src/components/common/SSEStatusIndicator.vue
- [x] src/components/common/LanguageSwitcher.vue

### Step 13: LoginView
- [x] src/views/LoginView.vue (매장 식별자, 사용자명, 비밀번호 폼)

### Step 14: DashboardView + TableCard
- [x] src/views/DashboardView.vue (테이블 그리드, 요약 통계)
- [x] src/components/dashboard/TableCard.vue (NEW 뱃지, 주문 미리보기)

### Step 15: OrderDetailModal
- [x] src/components/dashboard/OrderDetailModal.vue (주문 목록, 상태 변경, 삭제)

### Step 16: TableSetupDialog
- [x] src/components/dashboard/TableSetupDialog.vue (테이블 번호, 비밀번호 설정)

### Step 17: OrderHistoryPanel
- [x] src/components/dashboard/OrderHistoryPanel.vue (날짜 필터, 과거 주문 목록)

### Step 18: MenuManageView + 하위 컴포넌트
- [x] src/views/MenuManageView.vue (카테고리 + 메뉴 목록)
- [x] src/components/menu/CategoryManageSection.vue (drag-and-drop 순서 변경)
- [x] src/components/menu/MenuFormDialog.vue (메뉴 추가/수정 폼)

### Step 19: UserManageView + UserFormDialog
- [x] src/views/UserManageView.vue (사용자 목록 테이블)
- [x] src/components/user/UserFormDialog.vue (사용자 추가/수정 폼)

### Step 20: 컴포넌트 테스트
- [x] tests/components/LoginView.test.ts
- [x] tests/components/OrderStatusBadge.test.ts

### Step 21: 앱 엔트리
- [x] src/main.ts (앱 초기화, 플러그인 등록, 글로벌 에러 핸들러)
- [x] src/App.vue (루트 컴포넌트)
- [x] index.html (보안 메타 태그)

### Step 22: 코드 생성 요약 문서
- [x] aidlc-docs/construction/frontend-admin/code/code-generation-summary.md

---

## 스토리 커버리지

| 스토리 ID | 스토리명 | 커버 Step |
|-----------|---------|----------|
| US-O01 | 관리자 로그인 | 10, 13 |
| US-O02 | 실시간 주문 모니터링 | 8, 12, 14 |
| US-O03 | 주문 상태 변경 | 12, 15 |
| US-O04 | 주문 상세 보기 | 15 |
| US-O05 | 주문 삭제 | 15 |
| US-O06 | 테이블 초기 설정 | 16 |
| US-O07 | 테이블 이용 완료 처리 | 14 |
| US-O08 | 과거 주문 내역 조회 | 17 |
| US-O09 | 메뉴 등록 | 18 |
| US-O10 | 메뉴 수정 및 삭제 | 18 |
| US-O11 | 관리자 계정 관리 | 19 |
| US-M01 | 매니저 로그인 | 10, 13 |
| US-M02 | 실시간 주문 모니터링 (매니저) | 8, 12, 14 |
| US-M03 | 테이블 이용 완료 처리 (매니저) | 14 |
| US-M04 | 과거 주문 내역 조회 (매니저) | 17 |

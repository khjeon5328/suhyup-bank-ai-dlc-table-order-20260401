# Code Generation Plan - Unit 3: frontend-customer

> 담당자: 국현

## Unit Context
- **유닛**: frontend-customer (고객용 Vue.js SPA)
- **기술 스택**: Vue.js 3 + Pinia + Vue Router + Vite + Axios
- **코드 위치**: `frontend-customer/`
- **스토리**: US-C01 ~ US-C08 (8개)

## Generation Steps

### Step 1: 프로젝트 구조 및 설정
- [x] Vite + Vue 3 프로젝트 초기화 (package.json, vite.config.js)
- [x] index.html (보안 메타 태그 포함)

### Step 2: 핵심 설정 파일
- [x] main.js (앱 엔트리포인트, 글로벌 에러 핸들러)
- [x] App.vue (루트 컴포넌트, 하단 네비게이션)
- [x] router/index.js (라우터 설정, 네비게이션 가드)

### Step 3: 유틸리티 및 서비스 레이어
- [x] services/apiClient.js (Axios 인스턴스, 인터셉터)
- [x] services/authService.js
- [x] services/menuService.js
- [x] services/orderService.js
- [x] services/sseService.js
- [x] utils/logger.js
- [x] utils/validators.js
- [x] utils/formatters.js

### Step 4: Pinia 스토어
- [x] stores/authStore.js (인증, localStorage 영속)
- [x] stores/cartStore.js (장바구니, localStorage 영속)
- [x] stores/orderStore.js (주문, SSE 연동)

### Step 5: 인증 컴포넌트 (US-C01)
- [x] views/LoginSetupView.vue

### Step 6: 메뉴 컴포넌트 (US-C02, US-C03)
- [x] views/MenuView.vue
- [x] components/CategoryTabs.vue
- [x] components/MenuCard.vue
- [x] components/MenuDetailModal.vue

### Step 7: 장바구니 컴포넌트 (US-C04, US-C05)
- [x] views/CartView.vue
- [x] components/CartItemRow.vue

### Step 8: 주문 컴포넌트 (US-C06)
- [x] views/OrderConfirmView.vue
- [x] views/OrderResultView.vue

### Step 9: 주문 내역 컴포넌트 (US-C07, US-C08)
- [x] views/OrderHistoryView.vue
- [x] components/OrderCard.vue
- [x] components/OrderStatusBadge.vue

### Step 10: 단위 테스트
- [x] tests/stores/cartStore.test.js
- [x] tests/stores/authStore.test.js
- [x] tests/utils/formatters.test.js
- [x] tests/utils/validators.test.js

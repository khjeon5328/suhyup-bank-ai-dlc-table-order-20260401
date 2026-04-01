# Unit 3: frontend-customer - 프론트엔드 컴포넌트 설계

> 담당자: 국현

---

## 1. 페이지 구조

```
App.vue
├── LoginSetupView.vue        # 태블릿 초기 설정 (1회)
├── MenuView.vue              # 메뉴 조회 (기본 화면)
│   ├── CategoryTabs.vue
│   ├── MenuGrid.vue
│   │   └── MenuCard.vue
│   └── MenuDetailModal.vue
├── CartView.vue              # 장바구니
│   ├── CartItemList.vue
│   │   └── CartItemRow.vue
│   └── CartSummary.vue
├── OrderConfirmView.vue      # 주문 확인
├── OrderResultView.vue       # 주문 결과 (5초 후 리다이렉트)
└── OrderHistoryView.vue      # 주문 내역
    └── OrderCard.vue
        └── OrderStatusBadge.vue
```

---

## 2. 라우터 구조

| 경로 | 컴포넌트 | 설명 | 인증 필요 |
|------|---------|------|-----------|
| `/setup` | LoginSetupView | 태블릿 초기 설정 | No |
| `/` | MenuView | 메뉴 조회 (기본) | Yes (테이블 토큰) |
| `/menu/:id` | MenuDetailModal | 메뉴 상세 (모달) | Yes |
| `/cart` | CartView | 장바구니 | Yes |
| `/order/confirm` | OrderConfirmView | 주문 확인 | Yes |
| `/order/result/:orderId` | OrderResultView | 주문 결과 | Yes |
| `/orders` | OrderHistoryView | 주문 내역 | Yes |

**네비게이션 가드**: 토큰이 없으면 `/setup`으로 리다이렉트

---

## 3. 컴포넌트 상세

### 3.1 LoginSetupView.vue
**목적**: 태블릿 초기 설정 (관리자가 1회 수행)

**Props**: 없음

**State**:
- `storeCode: string` — 매장 식별 코드
- `tableNo: number` — 테이블 번호
- `password: string` — 테이블 비밀번호
- `isLoading: boolean`
- `errorMessage: string`

**사용자 흐름**:
1. 매장 코드, 테이블 번호, 비밀번호 입력
2. "설정 완료" 버튼 탭
3. POST `/api/v1/auth/login/table` 호출
4. 성공 시: 토큰 + 설정 정보 localStorage 저장 → `/` 이동
5. 실패 시: 에러 메시지 표시

**API 연동**: `POST /api/v1/auth/login/table`

---

### 3.2 MenuView.vue (기본 화면)
**목적**: 카테고리별 메뉴 조회

**State**:
- `categories: Category[]`
- `menus: Menu[]`
- `activeCategory: number` — 선택된 카테고리 ID
- `isLoading: boolean`

**사용자 흐름**:
1. 페이지 로드 시 카테고리 + 메뉴 목록 조회
2. 카테고리 탭 탭 → 해당 카테고리 메뉴 필터링
3. 메뉴 카드 탭 → MenuDetailModal 표시
4. "추가" 버튼 탭 → 장바구니에 추가

**API 연동**:
- `GET /api/v1/stores/{storeId}/menus/categories`
- `GET /api/v1/stores/{storeId}/menus?category={categoryId}`

---

### 3.3 CategoryTabs.vue
**목적**: 카테고리 탭 네비게이션

**Props**:
- `categories: Category[]`
- `activeId: number`

**Emits**: `@select(categoryId: number)`

---

### 3.4 MenuCard.vue
**목적**: 개별 메뉴 카드 표시

**Props**:
- `menu: Menu` (name, price, image_url)

**Emits**:
- `@click` — 상세 보기
- `@add-to-cart` — 장바구니 추가

**UI**: 카드 형태, 이미지 + 메뉴명 + 가격, "추가" 버튼 (44x44px 이상)

---

### 3.5 MenuDetailModal.vue
**목적**: 메뉴 상세 정보 모달

**Props**:
- `menu: Menu` (name, price, description, image_url)
- `visible: boolean`

**Emits**:
- `@close`
- `@add-to-cart`

**UI**: 큰 이미지, 메뉴명, 가격, 설명, "장바구니에 추가" 버튼

---

### 3.6 CartView.vue
**목적**: 장바구니 관리

**State**: Pinia `cartStore`에서 가져옴

**사용자 흐름**:
1. 장바구니 항목 목록 표시
2. 수량 +/- 버튼으로 조절
3. 삭제 버튼으로 개별 항목 삭제
4. "전체 비우기" 버튼
5. 총 금액 실시간 표시
6. "주문하기" 버튼 → OrderConfirmView 이동

---

### 3.7 CartItemRow.vue
**목적**: 장바구니 개별 항목

**Props**:
- `item: CartItem` (menuId, name, price, quantity, imageUrl)

**Emits**:
- `@increase`
- `@decrease`
- `@remove`

**UI**: 이미지 + 메뉴명 + 단가 + 수량 조절 버튼 + 소계 + 삭제 버튼

---

### 3.8 OrderConfirmView.vue
**목적**: 주문 최종 확인

**State**: Pinia `cartStore`에서 가져옴

**사용자 흐름**:
1. 장바구니 내용 최종 확인 (읽기 전용)
2. 총 금액 표시
3. "주문 확정" 버튼 탭
4. POST `/api/v1/stores/{storeId}/orders` 호출
5. 성공 → OrderResultView 이동
6. 실패 → 에러 메시지 표시, 장바구니 유지

**API 연동**: `POST /api/v1/stores/{storeId}/orders`

---

### 3.9 OrderResultView.vue
**목적**: 주문 성공 결과 표시

**Props (route params)**:
- `orderId: string`

**State**:
- `orderNo: string`
- `countdown: number` (5초 카운트다운)

**사용자 흐름**:
1. 주문 번호 표시
2. 장바구니 자동 비우기
3. 5초 카운트다운 표시
4. 5초 후 `/` (메뉴 화면)으로 자동 리다이렉트

---

### 3.10 OrderHistoryView.vue
**목적**: 현재 세션 주문 내역 조회

**State**:
- `orders: Order[]`
- `isLoading: boolean`
- `page: number`

**사용자 흐름**:
1. 현재 세션 주문 목록 조회
2. 주문 시간 순 정렬
3. 각 주문 카드에 주문 번호, 시각, 메뉴/수량, 금액, 상태 표시
4. SSE로 주문 상태 실시간 업데이트
5. 무한 스크롤 또는 페이지네이션

**API 연동**:
- `GET /api/v1/stores/{storeId}/orders?session_id={sessionId}`
- `SSE /api/v1/stores/{storeId}/events/table/{tableId}`

---

### 3.11 OrderStatusBadge.vue
**목적**: 주문 상태 뱃지

**Props**:
- `status: 'pending' | 'preparing' | 'completed'`

**UI**:
- pending: 노란색 "대기중"
- preparing: 파란색 "준비중"
- completed: 초록색 "완료"

---

## 4. Pinia 스토어

### 4.1 authStore
```
State:
  - token: string | null
  - storeId: number | null
  - tableId: number | null
  - sessionId: number | null
  - storeCode: string | null
  - tableNo: number | null

Actions:
  - login(storeCode, tableNo, password) → API 호출, 토큰 저장
  - logout() → 토큰 삭제
  - loadFromStorage() → localStorage에서 복원
  - isAuthenticated() → boolean

Persistence: localStorage
```

### 4.2 cartStore
```
State:
  - items: CartItem[] (menuId, name, price, quantity, imageUrl)
  - 
Getters:
  - totalAmount → 총 금액 계산
  - totalItems → 총 수량
  - isEmpty → 비어있는지

Actions:
  - addItem(menu) → 추가 (이미 있으면 수량+1)
  - removeItem(menuId) → 삭제
  - increaseQuantity(menuId)
  - decreaseQuantity(menuId) → 1이면 삭제
  - clearCart()

Persistence: localStorage (페이지 새로고침 유지)
```

### 4.3 orderStore
```
State:
  - currentOrders: Order[]
  - isLoading: boolean

Actions:
  - createOrder(items) → API 호출
  - fetchOrders(sessionId) → 주문 목록 조회
  - updateOrderStatus(orderId, status) → SSE 이벤트 처리

SSE Integration:
  - connectSSE() → SSE 연결
  - handleOrderEvent(event) → 주문 상태 업데이트
```

---

## 5. API 서비스 레이어

### apiClient.js
```
- baseURL: 환경변수에서 설정
- 요청 인터셉터: Authorization 헤더에 JWT 토큰 추가
- 응답 인터셉터: 401 시 /setup으로 리다이렉트
- 에러 핸들링: 공통 에러 처리
```

### 서비스 모듈
| 서비스 | 메서드 | API 엔드포인트 |
|--------|--------|---------------|
| authService | login(storeCode, tableNo, password) | POST /auth/login/table |
| menuService | getCategories(storeId) | GET /stores/{id}/menus/categories |
| menuService | getMenus(storeId, categoryId?) | GET /stores/{id}/menus |
| menuService | getMenu(storeId, menuId) | GET /stores/{id}/menus/{menuId} |
| orderService | createOrder(storeId, data) | POST /stores/{id}/orders |
| orderService | getOrders(storeId, sessionId) | GET /stores/{id}/orders |
| sseService | connectTable(storeId, tableId) | GET /stores/{id}/events/table/{tableId} |

---

## 6. SSE 이벤트 처리

### 수신 이벤트
| 이벤트 타입 | 데이터 | 처리 |
|------------|--------|------|
| order_status_changed | {orderId, status} | orderStore에서 해당 주문 상태 업데이트 |
| session_ended | {tableId} | 세션 종료 알림, 장바구니 비우기, 로그인 화면 이동 |

### 연결 관리
- 페이지 로드 시 자동 연결
- 연결 끊김 시 3초 후 자동 재연결
- 최대 재연결 시도: 10회
- 페이지 언로드 시 연결 해제

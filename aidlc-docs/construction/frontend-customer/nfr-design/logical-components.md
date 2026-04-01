# Unit 3: frontend-customer - Logical Components

> 담당자: 국현

---

## 아키텍처 레이어

```
+--------------------------------------------------+
|                  Views (Pages)                    |
|  LoginSetup | Menu | Cart | OrderConfirm | ...   |
+--------------------------------------------------+
|               Components (UI)                     |
|  CategoryTabs | MenuCard | CartItemRow | ...      |
+--------------------------------------------------+
|              Composables (Logic)                  |
|  useAuth | useCart | useSSE | useErrorHandler     |
+--------------------------------------------------+
|             Stores (State - Pinia)                |
|  authStore | cartStore | orderStore               |
+--------------------------------------------------+
|            Services (API Layer)                   |
|  apiClient | authService | menuService | ...      |
+--------------------------------------------------+
|              Utils (Helpers)                       |
|  logger | validators | formatters                 |
+--------------------------------------------------+
```

---

## Composables 정의

### useAuth
- `isAuthenticated` — 인증 상태 확인
- `autoLogin()` — localStorage에서 토큰 복원 및 검증
- `requireAuth()` — 라우터 가드용

### useCart
- `addToCart(menu)` — 장바구니 추가 (cartStore 래핑)
- `cartBadgeCount` — 네비게이션 뱃지용 총 수량

### useSSE
- `connect(storeId, tableId)` — SSE 연결
- `disconnect()` — 연결 해제
- `onEvent(type, handler)` — 이벤트 핸들러 등록
- 자동 재연결 로직 내장

### useErrorHandler
- `handleApiError(error)` — API 에러 분류 및 처리
- `showError(message)` — 사용자 에러 메시지 표시
- `showSuccess(message)` — 성공 메시지 표시

---

## Utils 정의

### logger
- `info(component, action, message)` — 정보 로그
- `error(component, action, message, error?)` — 에러 로그
- 프로덕션에서 민감 정보 필터링

### validators
- `validateStoreCode(value)` — 매장 코드 검증
- `validateTableNo(value)` — 테이블 번호 검증
- `validatePassword(value)` — 비밀번호 검증

### formatters
- `formatPrice(amount)` — 가격 포맷 (예: "12,000원")
- `formatDateTime(date)` — 날짜/시간 포맷
- `formatOrderNo(orderNo)` — 주문 번호 포맷

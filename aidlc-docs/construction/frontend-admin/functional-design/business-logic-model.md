# frontend-admin 비즈니스 로직 모델

> 담당자: 수민 | Unit 4: 관리자용 프론트엔드

---

## 1. 인증 플로우

### 1.1 로그인 플로우
```
사용자 입력 (store_identifier, username, password)
    │
    ▼
LoginView → authStore.login()
    │
    ▼
authApi.login(credentials)
    │
    ├── 성공 (200) ──→ Access Token → Pinia 메모리 저장
    │                   Refresh Token → httpOnly Cookie (서버 설정)
    │                   사용자 정보 → authStore.user
    │                   │
    │                   ▼
    │              router.push('/') → 대시보드
    │              sseService.connect() → SSE 연결 시작
    │
    └── 실패 (401/500) ──→ ElMessage.error(에러 메시지)
```

### 1.2 토큰 갱신 플로우
```
API 요청 → 401 응답 수신
    │
    ▼
axios interceptor (응답)
    │
    ▼
authApi.refresh() (httpOnly Cookie 자동 전송)
    │
    ├── 성공 ──→ 새 Access Token → Pinia 저장
    │            대기 중인 요청 재시도 (큐 패턴)
    │
    └── 실패 ──→ authStore.logout()
                  router.push('/login')
```

### 1.3 로그아웃 플로우
```
사용자 로그아웃 클릭 또는 세션 만료
    │
    ▼
authStore.logout()
    │
    ├── sseService.disconnect()
    ├── authApi.logout() (서버에 Refresh Token 무효화 요청)
    ├── Pinia 상태 초기화 (token, user)
    └── router.push('/login')
```

---

## 2. 주문 모니터링 플로우

### 2.1 대시보드 초기화
```
DashboardView mounted
    │
    ▼
orderStore.fetchAllTables()
    │
    ▼
tableApi.getAllTables() → 테이블 목록 수신
    │
    ▼
각 테이블별 orderApi.getOrders(tableId) → 주문 데이터 로드
    │
    ▼
테이블 카드 그리드 렌더링 (TableCard 컴포넌트)
    │
    ▼
SSE 연결 확인 (sseService.isConnected)
```

### 2.2 SSE: order_created 이벤트
```
SSE 수신: { type: 'order_created', data: { order, table_id } }
    │
    ▼
orderStore.handleOrderCreated(event)
    │
    ├── 해당 테이블의 orders 배열에 새 주문 추가
    ├── total_amount 재계산
    ├── status_counts.pending += 1
    ├── has_new_order = true (NEW 뱃지)
    └── 테이블 카드 pulse 애니메이션 트리거
```

### 2.3 주문 상태 변경
```
사용자가 OrderStatusButton 클릭
    │
    ▼
orderStore.updateOrderStatus(orderId, newStatus)
    │
    ▼
orderApi.updateStatus(orderId, newStatus)
    │
    ├── 성공 ──→ 로컬 상태 업데이트
    │            status_counts 재계산
    │            ElMessage.success('상태가 변경되었습니다')
    │
    └── 실패 ──→ ElMessage.error(에러 메시지)
```

### 2.4 주문 삭제 (owner만)
```
사용자가 삭제 버튼 클릭
    │
    ▼
ElMessageBox.confirm('주문을 삭제하시겠습니까?')
    │
    ├── 확인 ──→ orderStore.deleteOrder(orderId)
    │            │
    │            ▼
    │            orderApi.deleteOrder(orderId)
    │            │
    │            ├── 성공 ──→ orders 배열에서 제거
    │            │            total_amount 재계산
    │            │            ElMessage.success
    │            │
    │            └── 실패 ──→ ElMessage.error
    │
    └── 취소 ──→ (아무 동작 없음)
```

### 2.5 주문 상세 보기
```
사용자가 테이블 카드 클릭
    │
    ▼
OrderDetailModal 열기
    │
    ├── 테이블 번호, 세션 정보 표시
    ├── 주문 목록 (시간순 정렬)
    │   ├── 주문 번호, 시각
    │   ├── 메뉴 목록 (메뉴명, 수량, 단가)
    │   ├── 주문 금액
    │   ├── OrderStatusBadge (상태 표시)
    │   └── OrderStatusButton (상태 변경)
    ├── 총 주문액
    ├── 주문 삭제 버튼 (owner만)
    └── 과거 내역 버튼 → OrderHistoryPanel
```

---

## 3. 테이블 관리 플로우

### 3.1 테이블 초기 설정 (owner만)
```
사용자가 빈 테이블 카드의 "설정" 버튼 클릭
    │
    ▼
TableSetupDialog 열기
    │
    ▼
테이블 번호, 비밀번호 입력
    │
    ▼
tableStore.setupTable(tableNumber, password)
    │
    ▼
tableApi.setupTable(data)
    │
    ├── 성공 ──→ 테이블 목록 갱신
    │            ElMessage.success
    │
    └── 실패 ──→ ElMessage.error
```

### 3.2 이용 완료 처리
```
사용자가 "이용 완료" 버튼 클릭
    │
    ▼
ElMessageBox.confirm('이용 완료 처리하시겠습니까?')
    │
    ├── 확인 ──→ tableStore.endSession(tableId)
    │            │
    │            ▼
    │            tableApi.endSession(tableId)
    │            │
    │            ├── 성공 ──→ 주문 내역 → 과거 이력 이동
    │            │            테이블 카드 리셋 (주문 0, 총액 0)
    │            │            ElMessage.success
    │            │
    │            └── 실패 ──→ ElMessage.error
    │
    └── 취소 ──→ (아무 동작 없음)
```

### 3.3 과거 내역 조회
```
사용자가 "과거 내역" 버튼 클릭
    │
    ▼
OrderHistoryPanel 열기 (사이드 패널)
    │
    ▼
tableStore.fetchHistory(tableId, dateRange?)
    │
    ▼
tableApi.getHistory(tableId, params)
    │
    ▼
과거 주문 목록 표시 (시간 역순)
    │
    ├── 날짜 필터 변경 → 재조회
    └── "닫기" 버튼 → 패널 닫기
```

---

## 4. 메뉴 관리 플로우

### 4.1 카테고리 CRUD
```
MenuManageView → CategoryManageSection
    │
    ├── 카테고리 목록 조회: menuStore.fetchCategories()
    │
    ├── 카테고리 생성: menuStore.createCategory(name)
    │   └── menuApi.createCategory(data) → 목록 갱신
    │
    ├── 카테고리 수정: menuStore.updateCategory(id, name)
    │   └── menuApi.updateCategory(id, data) → 목록 갱신
    │
    ├── 카테고리 삭제: menuStore.deleteCategory(id)
    │   ├── menu_count > 0 → 에러 ("메뉴가 있는 카테고리는 삭제할 수 없습니다")
    │   └── menu_count === 0 → 확인 후 삭제 → 목록 갱신
    │
    └── 카테고리 순서 변경: drag-and-drop → menuApi.updateCategoryOrder(updates)
```

### 4.2 메뉴 목록 및 CRUD
```
카테고리 선택 → menuStore.fetchMenus(categoryId)
    │
    ▼
메뉴 목록 표시 (테이블 형태)
    │
    ├── 메뉴 생성: "추가" 버튼 → MenuFormDialog (빈 폼)
    │   ├── 이미지 선택 시 → imageApi.upload(file) → image_url 획득
    │   └── 저장 → menuApi.createMenu(data) → 목록 갱신
    │
    ├── 메뉴 수정: "수정" 버튼 → MenuFormDialog (기존 데이터 채움)
    │   └── 저장 → menuApi.updateMenu(id, data) → 목록 갱신
    │
    ├── 메뉴 삭제: "삭제" 버튼 → 확인 다이얼로그
    │   └── 확인 → menuApi.deleteMenu(id) → 목록 갱신
    │
    └── 메뉴 순서 변경: drag-and-drop → menuApi.updateMenuOrder(updates)
```

---

## 5. 사용자 관리 플로우

### 5.1 사용자 목록 및 CRUD
```
UserManageView mounted
    │
    ▼
userStore.fetchUsers()
    │
    ▼
사용자 목록 표시 (테이블 형태)
    │
    ├── 사용자 생성: "추가" 버튼 → UserFormDialog (빈 폼)
    │   └── 저장 → userApi.createUser(data) → 목록 갱신
    │
    ├── 사용자 수정: "수정" 버튼 → UserFormDialog (기존 데이터)
    │   └── 저장 → userApi.updateUser(id, data) → 목록 갱신
    │
    └── 사용자 삭제: "삭제" 버튼
        ├── 자기 자신 → 삭제 불가 메시지
        └── 타인 → 확인 다이얼로그 → userApi.deleteUser(id) → 목록 갱신
```

---

## 6. Pinia Store 구조

### authStore
```
State:
  - token: string | null          // Access Token
  - user: AuthUser | null         // 로그인 사용자 정보
  - isLoading: boolean

Getters:
  - isAuthenticated: boolean
  - isOwner: boolean
  - isManager: boolean
  - userRole: UserRole | null

Actions:
  - login(credentials): Promise<void>
  - logout(): Promise<void>
  - refreshToken(): Promise<void>
  - fetchUserInfo(): Promise<void>
```

### orderStore
```
State:
  - tables: TableSummary[]        // 전체 테이블 요약
  - selectedTableOrders: Order[]  // 선택된 테이블의 주문 목록
  - isLoading: boolean
  - error: string | null

Actions:
  - fetchAllTables(): Promise<void>
  - fetchTableOrders(tableId): Promise<void>
  - updateOrderStatus(orderId, status): Promise<void>
  - deleteOrder(orderId): Promise<void>
  - handleSSEEvent(event: SSEEvent): void
  - clearNewOrderFlag(tableId): void
```

### tableStore
```
State:
  - tables: Table[]
  - history: OrderHistory[]
  - isLoading: boolean

Actions:
  - fetchTables(): Promise<void>
  - setupTable(data): Promise<void>
  - endSession(tableId): Promise<void>
  - fetchHistory(tableId, dateRange?): Promise<void>
```

### menuStore
```
State:
  - categories: Category[]
  - menus: Menu[]
  - selectedCategoryId: number | null
  - isLoading: boolean

Actions:
  - fetchCategories(): Promise<void>
  - createCategory(data): Promise<void>
  - updateCategory(id, data): Promise<void>
  - deleteCategory(id): Promise<void>
  - updateCategoryOrder(updates): Promise<void>
  - fetchMenus(categoryId): Promise<void>
  - createMenu(data): Promise<void>
  - updateMenu(id, data): Promise<void>
  - deleteMenu(id): Promise<void>
  - updateMenuOrder(updates): Promise<void>
```

### userStore
```
State:
  - users: User[]
  - isLoading: boolean

Actions:
  - fetchUsers(): Promise<void>
  - createUser(data): Promise<void>
  - updateUser(id, data): Promise<void>
  - deleteUser(id): Promise<void>
```

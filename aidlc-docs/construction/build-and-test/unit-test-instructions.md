# Unit Test Instructions - frontend-admin

> 담당자: 수민

---

## 1. 테스트 실행

```bash
cd frontend-admin
npm test
```

단일 실행 (watch 모드 비활성화):
```bash
npx jest --run
```

특정 파일만 실행:
```bash
npx jest tests/stores/authStore.test.ts
```

커버리지 리포트:
```bash
npx jest --coverage
```

## 2. 테스트 구조

```
tests/
├── services/                    # API 서비스 테스트 (4개)
│   ├── apiClient.test.ts        # 인터셉터, 401 큐 패턴, GET 재시도
│   ├── authApi.test.ts          # login, logout, refresh, getMe
│   ├── orderApi.test.ts         # getOrders, updateStatus, deleteOrder
│   └── sseService.test.ts       # connect, disconnect, 재연결, 이벤트 핸들링
├── stores/                      # Pinia 스토어 테스트 (5개)
│   ├── authStore.test.ts        # 로그인/로그아웃, 토큰 관리, getters
│   ├── orderStore.test.ts       # 주문 CRUD, SSE 이벤트 처리, ordersByTable
│   ├── tableStore.test.ts       # 테이블 목록, newOrderTableIds, endSession
│   ├── menuStore.test.ts        # 메뉴/카테고리 CRUD, 순서 변경
│   └── userStore.test.ts        # 사용자 CRUD, 역할 필터
├── composables/                 # Composable 테스트 (2개)
│   ├── useAsyncAction.test.ts   # loading/error 상태, 성공/실패 케이스
│   └── usePermission.test.ts    # 역할별 권한 체크 (owner/manager)
└── components/                  # 컴포넌트 테스트 (2개)
    ├── LoginView.test.ts        # 폼 렌더링, 유효성 검증, 로그인 호출
    └── OrderStatusBadge.test.ts # 상태별 색상/텍스트 렌더링
```

## 3. 테스트 카테고리별 상세

### 서비스 테스트 (4개 파일, ~12 테스트)

| 파일 | 주요 테스트 케이스 |
|------|------------------|
| apiClient.test.ts | Authorization 헤더 추가, 401 시 토큰 갱신, 동시 401 큐 처리, GET 재시도 |
| authApi.test.ts | login 성공/실패, refresh 호출, getMe 응답 |
| orderApi.test.ts | getOrders 파라미터, updateStatus 요청, deleteOrder 호출 |
| sseService.test.ts | EventSource 연결, 이벤트 파싱, 재연결 로직, disconnect |

### 스토어 테스트 (5개 파일, ~15 테스트)

| 파일 | 주요 테스트 케이스 |
|------|------------------|
| authStore.test.ts | setAccessToken, setUser, logout 초기화, isAuthenticated getter |
| orderStore.test.ts | fetchOrders, updateOrderStatus, addOrder (SSE), deleteOrder |
| tableStore.test.ts | fetchTables, addNewOrderTableId, clearNewOrderTableId, endSession |
| menuStore.test.ts | fetchCategories, fetchMenus, createMenu, updateMenuOrder |
| userStore.test.ts | fetchUsers, createUser, updateUser, deleteUser |

### Composable 테스트 (2개 파일, ~4 테스트)

| 파일 | 주요 테스트 케이스 |
|------|------------------|
| useAsyncAction.test.ts | 성공 시 loading 전환, 실패 시 error 설정, 반환값 확인 |
| usePermission.test.ts | owner 권한 체크, manager 권한 제한 확인 |

### 컴포넌트 테스트 (2개 파일, ~4 테스트)

| 파일 | 주요 테스트 케이스 |
|------|------------------|
| LoginView.test.ts | 폼 필드 렌더링, 빈 필드 유효성 검증, 로그인 버튼 클릭 |
| OrderStatusBadge.test.ts | pending/preparing/completed 상태별 렌더링 |

## 4. 예상 테스트 수

| 카테고리 | 파일 수 | 예상 테스트 수 |
|---------|--------|--------------|
| 서비스 | 4 | ~12 |
| 스토어 | 5 | ~15 |
| Composable | 2 | ~4 |
| 컴포넌트 | 2 | ~4 |
| **합계** | **13** | **~33** |

## 5. 커버리지 목표

- **목표**: 80% 이상 (line coverage 기준)
- **핵심 레이어**: services, stores, composables → 90% 이상 권장
- **컴포넌트**: 주요 로직 위주 테스트 → 70% 이상

## 6. 테스트 설정

```typescript
// jest.config.ts
export default {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
  },
  transform: {
    '^.+\\.vue$': '@vue/vue3-jest',
    '^.+\\.tsx?$': 'ts-jest',
  },
  setupFilesAfterSetup: ['<rootDir>/tests/setup.ts'],
}
```

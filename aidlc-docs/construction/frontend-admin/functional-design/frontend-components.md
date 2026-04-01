# frontend-admin 프론트엔드 컴포넌트 설계

> 담당자: 수민 | Unit 4: 관리자용 프론트엔드

---

## 1. 레이아웃 구조

### AppLayout 컴포넌트 계층
```
App.vue
├── LoginView (인증 전)
└── AppLayout (인증 후)
    ├── Sidebar (좌측 네비게이션)
    │   ├── 매장명 / 로고
    │   ├── 메뉴 항목 (역할 기반 동적 렌더링)
    │   │   ├── 대시보드 (전체)
    │   │   ├── 메뉴 관리 (owner만)
    │   │   └── 사용자 관리 (owner만)
    │   └── 로그아웃 버튼
    ├── TopBar (상단 바)
    │   ├── 페이지 제목
    │   ├── SSEStatusIndicator
    │   ├── LanguageSwitcher
    │   └── 사용자 정보 (이름, 역할)
    └── <router-view /> (메인 콘텐츠)
```

### 반응형 브레이크포인트
| 구분 | 범위 | Sidebar | 그리드 열 수 |
|------|------|---------|-------------|
| PC | 1280px+ | 고정 표시 (240px) | 4~5열 |
| 태블릿 | 768~1279px | 접이식 (햄버거 메뉴) | 2~3열 |

---

## 2. 라우트 설계

| 경로 | 컴포넌트 | 가드 | 접근 권한 |
|------|---------|------|----------|
| `/login` | LoginView | 비인증 가드 (인증 시 `/`로 리다이렉트) | 전체 |
| `/` | DashboardView | 인증 가드 | owner, manager |
| `/menus` | MenuManageView | 인증 + 역할 가드 | owner만 |
| `/users` | UserManageView | 인증 + 역할 가드 | owner만 |

### 라우트 가드 로직
```
beforeEach(to, from, next)
    │
    ├── to.path === '/login'
    │   ├── 인증됨 → next('/')
    │   └── 미인증 → next()
    │
    └── to.path !== '/login'
        ├── 미인증 → next('/login')
        └── 인증됨
            ├── to.meta.requiredRole && user.role !== requiredRole
            │   → next('/') (권한 없음 → 대시보드)
            └── next()
```

---

## 3. 페이지 컴포넌트

### 3.1 LoginView
```
LoginView
├── 로그인 폼
│   ├── 매장 식별자 입력 (el-input)
│   ├── 사용자명 입력 (el-input)
│   ├── 비밀번호 입력 (el-input type="password")
│   └── 로그인 버튼 (el-button, loading 상태)
└── 에러 메시지 영역
```

### 3.2 DashboardView
```
DashboardView
├── 상단 요약 (총 테이블 수, 활성 세션 수, 대기 주문 수)
├── 테이블 그리드 (el-row + el-col, 반응형)
│   └── TableCard (v-for="table in tables")
│       ├── 테이블 번호
│       ├── NEW 뱃지 (신규 주문 시)
│       ├── 총 주문액
│       ├── 상태별 주문 수 (OrderStatusBadge)
│       ├── 최신 주문 미리보기 (1~2건)
│       ├── "이용 완료" 버튼
│       ├── "설정" 버튼 (owner만, 빈 테이블)
│       └── "과거 내역" 버튼
├── OrderDetailModal (테이블 카드 클릭 시)
│   ├── 테이블 정보
│   ├── 주문 목록
│   │   ├── OrderStatusBadge
│   │   ├── OrderStatusButton
│   │   ├── 메뉴 항목 목록
│   │   └── 삭제 버튼 (owner만)
│   └── 총 주문액
├── OrderHistoryPanel (사이드 패널)
│   ├── 날짜 필터 (el-date-picker)
│   ├── 과거 주문 목록
│   └── 닫기 버튼
└── TableSetupDialog (owner만)
    ├── 테이블 번호 입력
    ├── 비밀번호 입력
    └── 저장/취소 버튼
```

### 3.3 MenuManageView (owner만)
```
MenuManageView
├── CategoryManageSection
│   ├── 카테고리 목록 (drag-and-drop 순서 변경)
│   ├── 카테고리 추가 인라인 폼
│   ├── 카테고리 수정/삭제 버튼
│   └── 선택된 카테고리 하이라이트
├── 메뉴 목록 (el-table)
│   ├── 이미지 썸네일
│   ├── 메뉴명, 가격, 설명
│   ├── 순서 변경 핸들 (drag-and-drop)
│   └── 수정/삭제 버튼
├── "메뉴 추가" 버튼
└── MenuFormDialog
    ├── 메뉴명 입력 (el-input)
    ├── 가격 입력 (el-input-number)
    ├── 설명 입력 (el-input type="textarea")
    ├── 카테고리 선택 (el-select)
    ├── 이미지 업로드 (el-upload)
    └── 저장/취소 버튼
```

### 3.4 UserManageView (owner만)
```
UserManageView
├── 사용자 목록 (el-table)
│   ├── 사용자명
│   ├── 역할 (뱃지)
│   ├── 생성일
│   └── 수정/삭제 버튼
├── "사용자 추가" 버튼
└── UserFormDialog
    ├── 사용자명 입력 (el-input)
    ├── 비밀번호 입력 (el-input, 수정 시 선택)
    ├── 역할 선택 (el-radio-group: owner/manager)
    └── 저장/취소 버튼
```

---

## 4. 공통 컴포넌트

### OrderStatusBadge
- 주문 상태를 색상 뱃지로 표시
- Props: `status: OrderStatus`
- pending → warning(주황), preparing → primary(파랑), completed → success(초록)

### OrderStatusButton
- 다음 상태로 변경하는 버튼
- Props: `status: OrderStatus`, `orderId: number`
- pending → "준비 시작" 버튼, preparing → "완료" 버튼, completed → 버튼 없음

### SSEStatusIndicator
- SSE 연결 상태 표시
- 연결됨: 초록 점 + "실시간 연결"
- 연결 끊김: 빨간 점 + "연결 끊김"

### LanguageSwitcher
- 언어 전환 드롭다운
- 한국어/English 선택
- 선택 시 vue-i18n locale 변경 + localStorage 저장

---

## 5. API 서비스 레이어

### apiClient (axios 인스턴스)
```typescript
// 기본 설정
baseURL: import.meta.env.VITE_API_BASE_URL
timeout: 10000
withCredentials: true  // httpOnly Cookie 전송

// 요청 인터셉터: Authorization 헤더에 Access Token 추가
// 응답 인터셉터: 401 시 토큰 갱신 + 요청 재시도 (큐 패턴)
```

### 서비스 모듈

| 서비스 | 파일 | 주요 메서드 |
|--------|------|------------|
| authApi | `services/authApi.ts` | login, logout, refresh, getMe |
| orderApi | `services/orderApi.ts` | getOrders, updateStatus, deleteOrder |
| tableApi | `services/tableApi.ts` | getTables, setupTable, endSession, getHistory |
| menuApi | `services/menuApi.ts` | getCategories, createCategory, updateCategory, deleteCategory, getMenus, createMenu, updateMenu, deleteMenu, updateMenuOrder, updateCategoryOrder |
| userApi | `services/userApi.ts` | getUsers, createUser, updateUser, deleteUser |
| imageApi | `services/imageApi.ts` | uploadImage |
| sseService | `services/sseService.ts` | connect, disconnect, onEvent, isConnected |

---

## 6. 다국어 (i18n) 설계

### vue-i18n 설정
```typescript
// src/i18n/index.ts
import { createI18n } from 'vue-i18n'
import ko from '@/locales/ko.json'
import en from '@/locales/en.json'

const i18n = createI18n({
  locale: localStorage.getItem('locale') || 'ko',
  fallbackLocale: 'ko',
  messages: { ko, en }
})
```

### Locale 파일 구조
```
src/locales/
├── ko.json    // 한국어
└── en.json    // 영어
```

### 키 네이밍 규칙
```json
{
  "common": { "save": "저장", "cancel": "취소", "delete": "삭제" },
  "auth": { "login": "로그인", "logout": "로그아웃" },
  "dashboard": { "title": "대시보드", "totalOrders": "총 주문액" },
  "menu": { "title": "메뉴 관리", "addMenu": "메뉴 추가" },
  "user": { "title": "사용자 관리", "addUser": "사용자 추가" },
  "order": { "pending": "대기중", "preparing": "준비중", "completed": "완료" }
}
```

### 컴포넌트 사용
```vue
<template>
  <h1>{{ $t('dashboard.title') }}</h1>
  <el-button>{{ $t('common.save') }}</el-button>
</template>
```

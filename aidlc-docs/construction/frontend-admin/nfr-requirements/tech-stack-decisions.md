# Unit 4: frontend-admin - Tech Stack Decisions

> 담당자: 수민

---

## 핵심 기술 스택

| 기술 | 버전 | 용도 | 선택 이유 |
|------|------|------|----------|
| Vue.js | 3.4+ | UI 프레임워크 | Composition API, TypeScript 완벽 지원, 관리자 UI 적합 |
| TypeScript | 5.x | 타입 안전성 | 컴파일 타임 에러 검출, IDE 자동완성, 리팩토링 안전성 |
| Pinia | 2.x | 상태 관리 | Vue 3 공식 상태 관리, TypeScript 네이티브 지원 |
| Vue Router | 4.x | 라우팅 | SPA 라우팅, 네비게이션 가드, 역할 기반 접근 제어 |
| Element Plus | 2.x | UI 컴포넌트 | 관리자 UI에 최적화된 테이블/폼/다이얼로그, i18n 내장 |
| vue-i18n | 9.x | 다국어 | Vue 3 Composition API 지원, 동적 locale 전환 |
| axios | 1.x | HTTP 클라이언트 | 인터셉터, 토큰 갱신 큐 패턴, 에러 핸들링 |
| Vite | 5.x | 빌드 도구 | 빠른 HMR, 최적화된 프로덕션 빌드, 청크 분리 |

## 테스트 도구

| 기술 | 버전 | 용도 |
|------|------|------|
| Jest | 29.x | 단위 테스트 프레임워크 |
| @vue/test-utils | 2.x | Vue 컴포넌트 테스트 유틸리티 |
| Cypress | 13.x | E2E 테스트 |

## 코드 품질 도구

| 기술 | 버전 | 용도 |
|------|------|------|
| ESLint | 8.x | 코드 린팅 (TypeScript + Vue 규칙) |
| Prettier | 3.x | 코드 포맷팅 |
| Husky | 9.x | Git hooks (pre-commit) |
| lint-staged | 15.x | 스테이징 파일만 린트/포맷 |

## 추가 라이브러리

| 기술 | 용도 |
|------|------|
| vuedraggable | 카테고리/메뉴 순서 drag-and-drop |
| dayjs | 날짜/시간 포맷팅 (경량) |

---

## 프로젝트 구조

```
frontend-admin/
├── public/
├── src/
│   ├── types/                    # TypeScript 타입 정의
│   │   ├── auth.ts
│   │   ├── order.ts
│   │   ├── table.ts
│   │   ├── menu.ts
│   │   ├── user.ts
│   │   ├── sse.ts
│   │   └── api.ts
│   ├── locales/                  # 다국어 리소스
│   │   ├── ko.json
│   │   └── en.json
│   ├── services/                 # API 서비스 레이어
│   │   ├── apiClient.ts
│   │   ├── authApi.ts
│   │   ├── orderApi.ts
│   │   ├── tableApi.ts
│   │   ├── menuApi.ts
│   │   ├── userApi.ts
│   │   ├── imageApi.ts
│   │   └── sseService.ts
│   ├── stores/                   # Pinia 상태 관리
│   │   ├── authStore.ts
│   │   ├── orderStore.ts
│   │   ├── tableStore.ts
│   │   ├── menuStore.ts
│   │   └── userStore.ts
│   ├── composables/              # 재사용 로직
│   │   ├── useAuth.ts
│   │   ├── useSSE.ts
│   │   ├── useAsyncAction.ts
│   │   ├── usePermission.ts
│   │   ├── useConfirm.ts
│   │   └── useImageUpload.ts
│   ├── router/
│   │   └── index.ts
│   ├── components/
│   │   ├── layout/               # 레이아웃 컴포넌트
│   │   │   ├── AppLayout.vue
│   │   │   ├── Sidebar.vue
│   │   │   └── TopBar.vue
│   │   ├── common/               # 공통 컴포넌트
│   │   │   ├── OrderStatusBadge.vue
│   │   │   ├── OrderStatusButton.vue
│   │   │   ├── SSEStatusIndicator.vue
│   │   │   └── LanguageSwitcher.vue
│   │   ├── dashboard/            # 대시보드 전용
│   │   │   ├── TableCard.vue
│   │   │   ├── OrderDetailModal.vue
│   │   │   ├── TableSetupDialog.vue
│   │   │   └── OrderHistoryPanel.vue
│   │   ├── menu/                 # 메뉴 관리 전용
│   │   │   ├── CategoryManageSection.vue
│   │   │   └── MenuFormDialog.vue
│   │   └── user/                 # 사용자 관리 전용
│   │       └── UserFormDialog.vue
│   ├── views/
│   │   ├── LoginView.vue
│   │   ├── DashboardView.vue
│   │   ├── MenuManageView.vue
│   │   └── UserManageView.vue
│   ├── i18n/
│   │   └── index.ts
│   ├── App.vue
│   └── main.ts
├── tests/
│   ├── services/
│   ├── stores/
│   ├── composables/
│   └── components/
├── index.html
├── package.json
├── vite.config.ts
├── tsconfig.json
├── .eslintrc.cjs
├── .prettierrc
├── .env.example
└── .env.development
```

---

## 환경 변수

| 변수명 | 설명 | 예시 |
|--------|------|------|
| `VITE_API_BASE_URL` | 백엔드 REST API 기본 URL | `http://localhost:8000/api/v1` |
| `VITE_SSE_BASE_URL` | SSE 이벤트 스트림 기본 URL | `http://localhost:8000/api/v1/sse` |

```env
# .env.development
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_SSE_BASE_URL=http://localhost:8000/api/v1/sse
```

---

## TypeScript 설정

```jsonc
// tsconfig.json 핵심 설정
{
  "compilerOptions": {
    "strict": true,
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "preserve",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

---

## 브라우저 지원

| 브라우저 | 최소 버전 |
|---------|----------|
| Chrome | 90+ |
| Firefox | 90+ |
| Safari | 15+ |
| Edge | 90+ |

---

## 의존성 관리
- package-lock.json 커밋
- 정확한 버전 고정 (^, ~ 미사용)
- npm audit 정기 실행

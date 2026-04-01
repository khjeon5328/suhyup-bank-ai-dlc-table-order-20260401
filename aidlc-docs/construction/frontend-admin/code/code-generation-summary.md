# Unit 4: frontend-admin - Code Generation Summary

> 담당자: 수민

---

## 생성 파일 목록 (~55개)

### 프로젝트 설정 (7개)
| # | 파일 | 설명 |
|---|------|------|
| 1 | `package.json` | 의존성 및 스크립트 정의 |
| 2 | `vite.config.ts` | Vite 빌드 설정, Element Plus auto-import, manual chunks |
| 3 | `tsconfig.json` | TypeScript strict 모드, ES2020, bundler moduleResolution |
| 4 | `.eslintrc.cjs` | ESLint 규칙 (TypeScript + Vue) |
| 5 | `.prettierrc` | Prettier 포맷팅 규칙 |
| 6 | `.env.example` | 환경 변수 템플릿 |
| 7 | `.env.development` | 개발 환경 변수 |

### TypeScript 타입 (7개)
| # | 파일 | 설명 |
|---|------|------|
| 8 | `src/types/auth.ts` | LoginCredentials, AuthTokens, AuthUser, UserRole |
| 9 | `src/types/order.ts` | Order, OrderItem, OrderStatus, OrderHistory, OrderStatusCount |
| 10 | `src/types/table.ts` | Table, TableSession, TableSummary |
| 11 | `src/types/menu.ts` | Menu, MenuCreateRequest, Category, CategoryCreateRequest |
| 12 | `src/types/user.ts` | User, UserCreateRequest, UserUpdateRequest |
| 13 | `src/types/sse.ts` | SSEEvent, SSEEventType |
| 14 | `src/types/api.ts` | ApiResponse, ApiError, PaginatedResponse, DateRange |

### 다국어 (3개)
| # | 파일 | 설명 |
|---|------|------|
| 15 | `src/locales/ko.json` | 한국어 리소스 |
| 16 | `src/locales/en.json` | 영어 리소스 |
| 17 | `src/i18n/index.ts` | vue-i18n 설정, localStorage 연동 |

### API 서비스 (8개)
| # | 파일 | 설명 |
|---|------|------|
| 18 | `src/services/apiClient.ts` | Axios 인스턴스, 인터셉터, 401 큐 패턴 |
| 19 | `src/services/authApi.ts` | login, logout, refresh, getMe |
| 20 | `src/services/orderApi.ts` | getOrders, updateStatus, deleteOrder |
| 21 | `src/services/tableApi.ts` | getTables, setupTable, endSession, getHistory |
| 22 | `src/services/menuApi.ts` | 카테고리/메뉴 CRUD + 순서 변경 |
| 23 | `src/services/userApi.ts` | 사용자 CRUD |
| 24 | `src/services/imageApi.ts` | 이미지 업로드 |
| 25 | `src/services/sseService.ts` | SSE 연결, 이벤트 핸들링, 재연결 |

### Pinia 스토어 (5개)
| # | 파일 | 설명 |
|---|------|------|
| 26 | `src/stores/authStore.ts` | 인증 상태 (accessToken 메모리, user) |
| 27 | `src/stores/orderStore.ts` | 주문 상태 (ordersByTable Map, SSE 연동) |
| 28 | `src/stores/tableStore.ts` | 테이블 상태 (tables, newOrderTableIds Set) |
| 29 | `src/stores/menuStore.ts` | 메뉴 상태 (menus, categories, selectedCategory) |
| 30 | `src/stores/userStore.ts` | 사용자 상태 (users) |

### Composables (6개)
| # | 파일 | 설명 |
|---|------|------|
| 31 | `src/composables/useAuth.ts` | 인증 플로우 캡슐화 |
| 32 | `src/composables/useSSE.ts` | SSE 연결/이벤트 관리 |
| 33 | `src/composables/useAsyncAction.ts` | 비동기 loading/error 패턴 |
| 34 | `src/composables/usePermission.ts` | 역할 기반 권한 체크 |
| 35 | `src/composables/useConfirm.ts` | 확인 다이얼로그 래핑 |
| 36 | `src/composables/useImageUpload.ts` | 이미지 업로드 관리 |

### 라우터 (1개)
| # | 파일 | 설명 |
|---|------|------|
| 37 | `src/router/index.ts` | 라우트 정의, 인증 + 역할 가드 |

### 레이아웃 컴포넌트 (3개)
| # | 파일 | 설명 |
|---|------|------|
| 38 | `src/components/layout/AppLayout.vue` | Sidebar + TopBar + router-view |
| 39 | `src/components/layout/Sidebar.vue` | 역할 기반 네비게이션 메뉴 |
| 40 | `src/components/layout/TopBar.vue` | SSE 상태, 언어 전환, 사용자 정보 |

### 공통 컴포넌트 (4개)
| # | 파일 | 설명 |
|---|------|------|
| 41 | `src/components/common/OrderStatusBadge.vue` | 주문 상태 색상 뱃지 |
| 42 | `src/components/common/OrderStatusButton.vue` | 상태 전이 버튼 |
| 43 | `src/components/common/SSEStatusIndicator.vue` | SSE 연결 상태 표시 |
| 44 | `src/components/common/LanguageSwitcher.vue` | 언어 전환 드롭다운 |

### 대시보드 컴포넌트 (4개)
| # | 파일 | 설명 |
|---|------|------|
| 45 | `src/components/dashboard/TableCard.vue` | 테이블 카드 (NEW 뱃지, 주문 미리보기) |
| 46 | `src/components/dashboard/OrderDetailModal.vue` | 주문 상세 모달 |
| 47 | `src/components/dashboard/TableSetupDialog.vue` | 테이블 설정 다이얼로그 |
| 48 | `src/components/dashboard/OrderHistoryPanel.vue` | 과거 주문 내역 패널 |

### 메뉴 관리 컴포넌트 (2개)
| # | 파일 | 설명 |
|---|------|------|
| 49 | `src/components/menu/CategoryManageSection.vue` | 카테고리 관리 (drag-and-drop) |
| 50 | `src/components/menu/MenuFormDialog.vue` | 메뉴 추가/수정 폼 |

### 사용자 관리 컴포넌트 (1개)
| # | 파일 | 설명 |
|---|------|------|
| 51 | `src/components/user/UserFormDialog.vue` | 사용자 추가/수정 폼 |

### 뷰 (4개)
| # | 파일 | 설명 |
|---|------|------|
| 52 | `src/views/LoginView.vue` | 로그인 페이지 |
| 53 | `src/views/DashboardView.vue` | 대시보드 (테이블 그리드) |
| 54 | `src/views/MenuManageView.vue` | 메뉴 관리 페이지 |
| 55 | `src/views/UserManageView.vue` | 사용자 관리 페이지 |

### 앱 엔트리 (3개)
| # | 파일 | 설명 |
|---|------|------|
| 56 | `src/main.ts` | 앱 초기화, 플러그인 등록 |
| 57 | `src/App.vue` | 루트 컴포넌트 |
| 58 | `index.html` | HTML 엔트리 (보안 메타 태그) |

### 테스트 (13개)
| # | 파일 | 설명 |
|---|------|------|
| 59 | `tests/services/apiClient.test.ts` | API 클라이언트 테스트 |
| 60 | `tests/services/authApi.test.ts` | 인증 API 테스트 |
| 61 | `tests/services/orderApi.test.ts` | 주문 API 테스트 |
| 62 | `tests/services/sseService.test.ts` | SSE 서비스 테스트 |
| 63 | `tests/stores/authStore.test.ts` | 인증 스토어 테스트 |
| 64 | `tests/stores/orderStore.test.ts` | 주문 스토어 테스트 |
| 65 | `tests/stores/tableStore.test.ts` | 테이블 스토어 테스트 |
| 66 | `tests/stores/menuStore.test.ts` | 메뉴 스토어 테스트 |
| 67 | `tests/stores/userStore.test.ts` | 사용자 스토어 테스트 |
| 68 | `tests/composables/useAsyncAction.test.ts` | useAsyncAction 테스트 |
| 69 | `tests/composables/usePermission.test.ts` | usePermission 테스트 |
| 70 | `tests/components/LoginView.test.ts` | 로그인 컴포넌트 테스트 |
| 71 | `tests/components/OrderStatusBadge.test.ts` | 상태 뱃지 컴포넌트 테스트 |

---

## 스토리 커버리지 (15/15)

| 스토리 ID | 스토리명 | 커버 여부 |
|-----------|---------|:---------:|
| US-O01 | 관리자 로그인 | ✅ |
| US-O02 | 실시간 주문 모니터링 | ✅ |
| US-O03 | 주문 상태 변경 | ✅ |
| US-O04 | 주문 상세 보기 | ✅ |
| US-O05 | 주문 삭제 | ✅ |
| US-O06 | 테이블 초기 설정 | ✅ |
| US-O07 | 테이블 이용 완료 처리 | ✅ |
| US-O08 | 과거 주문 내역 조회 | ✅ |
| US-O09 | 메뉴 등록 | ✅ |
| US-O10 | 메뉴 수정 및 삭제 | ✅ |
| US-O11 | 관리자 계정 관리 | ✅ |
| US-M01 | 매니저 로그인 | ✅ |
| US-M02 | 실시간 주문 모니터링 (매니저) | ✅ |
| US-M03 | 테이블 이용 완료 처리 (매니저) | ✅ |
| US-M04 | 과거 주문 내역 조회 (매니저) | ✅ |

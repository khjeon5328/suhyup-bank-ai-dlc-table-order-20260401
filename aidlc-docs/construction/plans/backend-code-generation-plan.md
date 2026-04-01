# Backend Code Generation Plan

## 유닛 정보
- **유닛명**: backend (백엔드 API 서버)
- **기술 스택**: Python 3.11+ / FastAPI / SQLAlchemy 2.0 / MySQL
- **코드 위치**: `backend/` (workspace root)
- **아키텍처**: 3-Layer (Router → Service → Repository)
- **담당 스토리**: 23개 전체

## 유닛 의존성
- **database 유닛**: SQLAlchemy 모델, Pydantic 스키마 (backend에서 참조)
- **참고**: database 유닛의 모델/스키마를 backend/app/models/에서 re-export

## 참조 아티팩트
- `aidlc-docs/construction/backend/functional-design/` (도메인 엔티티, 비즈니스 로직, 비즈니스 규칙)
- `aidlc-docs/construction/backend/nfr-requirements/` (NFR 요구사항, 기술 스택)
- `aidlc-docs/construction/backend/nfr-design/` (설계 패턴, 논리적 컴포넌트)

---

## Code Generation Steps

### Step 1: 프로젝트 구조 및 설정 파일
- [x] `backend/requirements.txt` — 의존성 목록
- [x] `backend/.env.example` — 환경 변수 템플릿
- [x] `backend/app/__init__.py`
- [x] `backend/app/config.py` — Pydantic Settings
- [x] `backend/app/main.py` — FastAPI 앱 엔트리포인트, 미들웨어, 라우터 등록

### Step 2: Core 모듈 (Cross-cutting)
- [x] `backend/app/core/__init__.py`
- [x] `backend/app/core/database.py` — async engine, session factory
- [x] `backend/app/core/exceptions.py` — 커스텀 예외 계층
- [x] `backend/app/core/security.py` — JWT 발급/검증, bcrypt 유틸리티
- [x] `backend/app/core/event_bus.py` — EventBus (asyncio.Queue 기반)
- [x] `backend/app/core/sse_manager.py` — SSEManager
- [x] `backend/app/core/dependencies.py` — DI 팩토리 (get_db, get_current_user 등)
- [x] `backend/app/core/logging_config.py` — structlog 설정

### Step 3: Middleware
- [x] `backend/app/middleware/__init__.py`
- [x] `backend/app/middleware/security_headers.py` — SECURITY-04 보안 헤더
- [x] `backend/app/middleware/request_id.py` — Request ID (contextvars)

### Step 4: SQLAlchemy 모델 및 Pydantic 스키마
- [x] `backend/app/models/__init__.py` — ORM 모델 정의
- [x] `backend/app/models/store.py`
- [x] `backend/app/models/user.py`
- [x] `backend/app/models/table.py`
- [x] `backend/app/models/table_session.py`
- [x] `backend/app/models/category.py`
- [x] `backend/app/models/menu.py`
- [x] `backend/app/models/order.py`
- [x] `backend/app/models/order_item.py`
- [x] `backend/app/models/order_history.py`
- [x] `backend/app/models/login_attempt.py`
- [x] `backend/app/schemas/__init__.py`
- [x] `backend/app/schemas/common.py` — 공통 응답, 에러 스키마
- [x] `backend/app/schemas/auth.py`
- [x] `backend/app/schemas/store.py`
- [x] `backend/app/schemas/table.py`
- [x] `backend/app/schemas/menu.py`
- [x] `backend/app/schemas/order.py`
- [x] `backend/app/schemas/user.py`
- [x] `backend/app/schemas/image.py`

### Step 5: Repository Layer
- [x] `backend/app/repositories/__init__.py`
- [x] `backend/app/repositories/store_repo.py`
- [x] `backend/app/repositories/user_repo.py`
- [x] `backend/app/repositories/table_repo.py`
- [x] `backend/app/repositories/session_repo.py`
- [x] `backend/app/repositories/category_repo.py`
- [x] `backend/app/repositories/menu_repo.py`
- [x] `backend/app/repositories/order_repo.py`
- [x] `backend/app/repositories/order_item_repo.py`
- [x] `backend/app/repositories/order_history_repo.py`
- [x] `backend/app/repositories/login_attempt_repo.py`

### Step 6: Service Layer
- [x] `backend/app/services/__init__.py`
- [x] `backend/app/services/auth_service.py` — US-O01, US-M01, US-C01
- [x] `backend/app/services/store_service.py`
- [x] `backend/app/services/table_service.py` — US-O06, US-O07, US-M03
- [x] `backend/app/services/menu_service.py` — US-C02, US-C03, US-O09, US-O10
- [x] `backend/app/services/order_service.py` — US-C06, US-C07, US-O02~O05, US-O08, US-M02, US-M04
- [x] `backend/app/services/user_service.py` — US-O11
- [x] `backend/app/services/image_service.py` — US-O09 (이미지)

### Step 7: Router Layer
- [x] `backend/app/routers/__init__.py`
- [x] `backend/app/routers/auth.py` — POST /login/admin, POST /login/table
- [x] `backend/app/routers/stores.py` — GET /stores/{id}
- [x] `backend/app/routers/tables.py` — GET/POST /tables, POST session/end, GET history
- [x] `backend/app/routers/menus.py` — GET/POST/PUT/DELETE /menus, categories
- [x] `backend/app/routers/orders.py` — GET/POST /orders, PATCH status, DELETE
- [x] `backend/app/routers/users.py` — GET/POST/PUT/DELETE /users
- [x] `backend/app/routers/images.py` — POST /presigned-url
- [x] `backend/app/routers/events.py` — GET /events/admin, GET /events/table/{id}

### Step 8: Unit Tests — Core & Repository
- [x] `backend/tests/__init__.py`
- [x] `backend/tests/conftest.py` — pytest fixtures (async DB, test client)
- [x] `backend/tests/test_core/` — security, exceptions, event_bus 테스트
- [x] `backend/tests/test_repositories/` — repository 레이어 테스트

### Step 9: Unit Tests — Service Layer
- [x] `backend/tests/test_services/test_auth_service.py`
- [x] `backend/tests/test_services/test_order_service.py`
- [x] `backend/tests/test_services/test_table_service.py`
- [x] `backend/tests/test_services/test_menu_service.py`
- [x] `backend/tests/test_services/test_user_service.py`

### Step 10: Unit Tests — Router Layer
- [x] `backend/tests/test_routers/test_auth_router.py`
- [x] `backend/tests/test_routers/test_order_router.py`
- [x] `backend/tests/test_routers/test_menu_router.py`
- [x] `backend/tests/test_routers/test_table_router.py`
- [x] `backend/tests/test_routers/test_user_router.py`

### Step 11: Documentation & Deployment
- [x] `aidlc-docs/construction/backend/code/code-generation-summary.md` — 코드 생성 요약
- [x] `backend/README.md` — 프로젝트 설명, 실행 방법

---

## 스토리 커버리지 추적

| 스토리 ID | 스토리명 | 구현 Step | 완료 |
|-----------|---------|----------|:----:|
| US-C01 | 테이블 태블릿 자동 로그인 | Step 6 (auth), Step 7 (auth) | [ ] |
| US-C02 | 카테고리별 메뉴 조회 | Step 6 (menu), Step 7 (menus) | [ ] |
| US-C03 | 메뉴 상세 정보 확인 | Step 6 (menu), Step 7 (menus) | [ ] |
| US-C04 | 장바구니에 메뉴 추가 | 클라이언트 전용 (backend N/A) | [x] |
| US-C05 | 장바구니 수량 조절 및 삭제 | 클라이언트 전용 (backend N/A) | [x] |
| US-C06 | 주문 생성 | Step 6 (order), Step 7 (orders) | [ ] |
| US-C07 | 주문 내역 조회 | Step 6 (order), Step 7 (orders) | [ ] |
| US-C08 | 주문 상태 실시간 업데이트 | Step 2 (SSE), Step 7 (events) | [ ] |
| US-O01 | 관리자 로그인 | Step 6 (auth), Step 7 (auth) | [ ] |
| US-O02 | 실시간 주문 모니터링 | Step 6 (order), Step 7 (events) | [ ] |
| US-O03 | 주문 상태 변경 | Step 6 (order), Step 7 (orders) | [ ] |
| US-O04 | 주문 상세 보기 | Step 6 (order), Step 7 (orders) | [ ] |
| US-O05 | 주문 삭제 | Step 6 (order), Step 7 (orders) | [ ] |
| US-O06 | 테이블 초기 설정 | Step 6 (table), Step 7 (tables) | [ ] |
| US-O07 | 테이블 이용 완료 처리 | Step 6 (table), Step 7 (tables) | [ ] |
| US-O08 | 과거 주문 내역 조회 | Step 6 (order), Step 7 (orders) | [ ] |
| US-O09 | 메뉴 등록 | Step 6 (menu, image), Step 7 (menus, images) | [ ] |
| US-O10 | 메뉴 수정 및 삭제 | Step 6 (menu), Step 7 (menus) | [ ] |
| US-O11 | 관리자 계정 관리 | Step 6 (user), Step 7 (users) | [ ] |
| US-M01 | 매니저 로그인 | Step 6 (auth), Step 7 (auth) | [ ] |
| US-M02 | 실시간 주문 모니터링 (매니저) | Step 6 (order), Step 7 (events) | [ ] |
| US-M03 | 테이블 이용 완료 처리 (매니저) | Step 6 (table), Step 7 (tables) | [ ] |
| US-M04 | 과거 주문 내역 조회 (매니저) | Step 6 (order), Step 7 (orders) | [ ] |

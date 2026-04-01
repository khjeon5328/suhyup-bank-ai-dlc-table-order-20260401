# Backend - 논리적 컴포넌트 구조

---

## 1. 전체 컴포넌트 맵

```
+------------------------------------------------------------------+
|                        FastAPI Application                        |
|                                                                    |
|  +------------------------------------------------------------+  |
|  |                    Middleware Stack                          |  |
|  |  SecurityHeaders > RequestID > RateLimit > CORS             |  |
|  +------------------------------------------------------------+  |
|                                                                    |
|  +------------------------------------------------------------+  |
|  |                    Router Layer                              |  |
|  |  auth_router | store_router | table_router | menu_router    |  |
|  |  order_router | user_router | image_router | sse_router     |  |
|  +-----------------------------+------------------------------+  |
|                                |                                  |
|  +-----------------------------v------------------------------+  |
|  |                   Auth Dependencies                         |  |
|  |  get_current_user | require_owner | require_admin           |  |
|  |  require_table | verify_store_access                        |  |
|  +-----------------------------+------------------------------+  |
|                                |                                  |
|  +-----------------------------v------------------------------+  |
|  |                    Service Layer                             |  |
|  |  AuthService | StoreService | TableService | MenuService    |  |
|  |  OrderService | UserService | ImageService                  |  |
|  +-----------------------------+------------------------------+  |
|                                |                                  |
|  +-----------------------------v------------------------------+  |
|  |                  Repository Layer                            |  |
|  |  StoreRepo | TableRepo | SessionRepo | MenuRepo             |  |
|  |  CategoryRepo | OrderRepo | OrderItemRepo | UserRepo        |  |
|  |  OrderHistoryRepo | LoginAttemptRepo                        |  |
|  +-----------------------------+------------------------------+  |
|                                |                                  |
|  +-----------------------------v------------------------------+  |
|  |                  Infrastructure                              |  |
|  |  AsyncSession (SQLAlchemy) | EventBus | SSEManager          |  |
|  |  S3Client (boto3) | Settings (Pydantic)                     |  |
|  +------------------------------------------------------------+  |
+------------------------------------------------------------------+
```

---

## 2. 미들웨어 스택

실행 순서 (외부 → 내부):

| 순서 | 미들웨어 | 책임 | SECURITY 매핑 |
|------|---------|------|--------------|
| 1 | SecurityHeadersMiddleware | CSP, HSTS, X-Content-Type-Options 등 주입 | SECURITY-04 |
| 2 | RequestIDMiddleware | UUID 생성 → contextvars 저장 → 응답 헤더 | SECURITY-03 |
| 3 | RateLimitMiddleware (slowapi) | IP 기반 전역 Rate Limiting | SECURITY-11 |
| 4 | CORSMiddleware | 환경별 origin 허용 정책 | SECURITY-08 |
| 5 | GlobalExceptionHandler | 미처리 예외 포착 → generic 응답 | SECURITY-09, 15 |

---

## 3. 라우터 컴포넌트

| 라우터 | 경로 접두사 | Auth 의존성 | 서비스 |
|--------|-----------|------------|--------|
| auth_router | /api/v1/auth | 없음 (공개) | AuthService |
| store_router | /api/v1/stores/{store_id} | get_current_user | StoreService |
| table_router | /api/v1/stores/{store_id}/tables | require_admin/owner | TableService |
| menu_router | /api/v1/stores/{store_id}/menus | 혼합 (조회:all, CUD:owner) | MenuService |
| order_router | /api/v1/stores/{store_id}/orders | 혼합 (생성:table, 관리:admin) | OrderService |
| user_router | /api/v1/stores/{store_id}/users | require_owner | UserService |
| image_router | /api/v1/stores/{store_id}/images | require_owner | ImageService |
| sse_router | /api/v1/stores/{store_id}/events | 혼합 (admin/table) | SSEManager |

---

## 4. 서비스 컴포넌트

| 서비스 | 의존성 (DI) | 핵심 책임 |
|--------|-----------|----------|
| AuthService | UserRepo, LoginAttemptRepo, Settings | 로그인, JWT 발급/검증, 브루트포스 검사 |
| StoreService | StoreRepo | 매장 정보 조회 |
| TableService | TableRepo, SessionRepo, OrderRepo, OrderHistoryRepo, EventBus | 테이블 설정, 세션 관리, 이용 완료 |
| MenuService | MenuRepo, CategoryRepo | 메뉴/카테고리 CRUD |
| OrderService | OrderRepo, OrderItemRepo, MenuRepo, SessionRepo, EventBus | 주문 생성/상태 변경/삭제 |
| UserService | UserRepo, AuthService | 계정 CRUD, 비밀번호 해싱 |
| ImageService | S3Client, Settings | Presigned URL 생성 |

---

## 5. Repository 컴포넌트

| Repository | 엔티티 | 주요 메서드 |
|-----------|--------|-----------|
| StoreRepo | Store | get_by_id, get_by_code |
| TableRepo | Table | create, get_by_store, get_by_store_and_no |
| SessionRepo | TableSession | create, get_active, deactivate |
| MenuRepo | Menu | create, get_by_store, get_by_id, update, soft_delete |
| CategoryRepo | Category | create, get_by_store, update, soft_delete |
| OrderRepo | Order | create, get_by_session, get_by_store, update_status, soft_delete, get_next_order_no |
| OrderItemRepo | OrderItem | bulk_create, get_by_order |
| OrderHistoryRepo | OrderHistory | bulk_create, get_by_table |
| UserRepo | User | create, get_by_store, get_by_username, update, soft_delete |
| LoginAttemptRepo | LoginAttempt | create, count_recent_by_ip, count_recent_by_account |

---

## 6. 인프라 컴포넌트

### 6.1 EventBus (싱글턴)

```
EventBus
  |
  +-- _queues: Dict[int, List[asyncio.Queue]]
  |     매장별 구독자 큐 목록
  |
  +-- publish(store_id, event)
  |     모든 구독자 큐에 이벤트 전달
  |
  +-- subscribe(store_id) -> AsyncGenerator
        새 큐 생성 → 이벤트 수신 대기
```

### 6.2 SSEManager (싱글턴)

```
SSEManager
  |
  +-- _event_bus: EventBus
  |
  +-- connect_admin(store_id)
  |     EventBus 구독 → 매장 전체 이벤트 스트림
  |
  +-- connect_table(store_id, table_id)
        EventBus 구독 → 해당 테이블 이벤트만 필터링
```

### 6.3 S3Client

```
S3Client
  |
  +-- _client: boto3.client("s3")
  +-- _bucket: str
  |
  +-- generate_presigned_url(store_id, filename, content_type)
        PUT presigned URL 생성 (300초 만료)
```

### 6.4 Settings (Pydantic Settings)

```
Settings
  |
  +-- DATABASE_URL: str
  +-- JWT_SECRET_KEY: str
  +-- JWT_ALGORITHM: str = "HS256"
  +-- JWT_ADMIN_EXPIRE_HOURS: int = 16
  +-- S3_BUCKET: str
  +-- S3_REGION: str
  +-- CORS_ORIGINS: List[str]
  +-- RATE_LIMIT_LOGIN: str = "20/15minutes"
  +-- RATE_LIMIT_GENERAL: str = "60/minute"
  +-- LOG_LEVEL: str = "INFO"
  +-- ENVIRONMENT: str = "development"
```

---

## 7. 파일 구조 (최종)

```
backend/
  app/
    __init__.py
    main.py                    # FastAPI 앱, 미들웨어 등록, 라우터 포함
    config.py                  # Pydantic Settings
    |
    routers/                   # Router Layer
      __init__.py
      auth.py
      stores.py
      tables.py
      menus.py
      orders.py
      users.py
      images.py
      events.py
    |
    services/                  # Service Layer
      __init__.py
      auth_service.py
      store_service.py
      table_service.py
      menu_service.py
      order_service.py
      user_service.py
      image_service.py
    |
    repositories/              # Repository Layer
      __init__.py
      store_repo.py
      table_repo.py
      session_repo.py
      menu_repo.py
      category_repo.py
      order_repo.py
      order_item_repo.py
      order_history_repo.py
      user_repo.py
      login_attempt_repo.py
    |
    middleware/                 # Middleware
      __init__.py
      security_headers.py
      request_id.py
    |
    core/                      # Cross-cutting
      __init__.py
      database.py              # async engine, session factory
      dependencies.py          # DI 팩토리 (get_db, get_service 등)
      exceptions.py            # 커스텀 예외 계층
      event_bus.py             # EventBus 싱글턴
      sse_manager.py           # SSEManager
      security.py              # JWT, bcrypt 유틸리티
      logging.py               # structlog 설정
    |
    schemas/                   # Pydantic 스키마 (요청/응답 DTO)
      __init__.py
      auth.py
      store.py
      table.py
      menu.py
      order.py
      user.py
      image.py
      common.py                # 공통 응답, 에러 스키마
    |
    models/                    # SQLAlchemy ORM 모델 (database 유닛 참조)
      __init__.py              # database 유닛의 모델 re-export
  |
  tests/                       # 단위 테스트
    __init__.py
    conftest.py                # pytest fixtures
    test_auth_service.py
    test_order_service.py
    test_table_service.py
    test_menu_service.py
    test_user_service.py
    test_routers/
      __init__.py
      test_auth_router.py
      test_order_router.py
      test_menu_router.py
  |
  requirements.txt
  .env.example
```

---

## 8. 의존성 주입 흐름도

```
main.py (앱 시작)
  |
  +-- Settings 로드 (.env)
  +-- AsyncEngine 생성
  +-- EventBus 싱글턴 생성
  +-- SSEManager 싱글턴 생성 (EventBus 주입)
  +-- S3Client 생성
  +-- 미들웨어 등록
  +-- 라우터 등록
  |
  v
[요청 수신]
  |
  +-- get_db_session() → AsyncSession
  +-- get_current_user(token) → TokenPayload
  +-- verify_store_access(store_id, user) → store_id
  +-- get_xxx_repository(db) → Repository
  +-- get_xxx_service(repo, event_bus, ...) → Service
  |
  v
[Router → Service → Repository → DB]
  |
  v
[응답 반환]
```

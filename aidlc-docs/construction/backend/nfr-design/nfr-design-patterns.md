# Backend - NFR 설계 패턴

---

## 1. 아키텍처 패턴: 3-Layer Architecture

### 레이어 구조

```
+--------------------------------------------------+
|                   Router Layer                    |
|  (FastAPI 라우터, 요청/응답 변환, 권한 검사)       |
+-------------------------+------------------------+
                          |
                          v
+-------------------------+------------------------+
|                  Service Layer                    |
|  (비즈니스 로직, 트랜잭션 관리, 이벤트 발행)       |
+-------------------------+------------------------+
                          |
                          v
+-------------------------+------------------------+
|                Repository Layer                   |
|  (데이터 접근, SQLAlchemy 쿼리, CRUD 연산)        |
+--------------------------------------------------+
```

### 레이어별 책임

| 레이어 | 책임 | 의존 대상 |
|--------|------|----------|
| Router | HTTP 요청 파싱, Pydantic 검증, 권한 검사, 응답 직렬화 | Service |
| Service | 비즈니스 로직, 트랜잭션 경계, SSE 이벤트 발행, 크로스 모듈 조율 | Repository, SSEManager |
| Repository | DB CRUD, SQLAlchemy 쿼리, 데이터 매핑 | SQLAlchemy Session |

### 레이어 규칙
- Router는 Service만 호출 (Repository 직접 접근 금지)
- Service는 Repository를 통해서만 DB 접근
- Repository는 비즈니스 로직 포함 금지 (순수 데이터 접근)
- 레이어 간 데이터 전달: Pydantic 스키마 사용

---

## 2. 보안 패턴

### 2.1 인증 미들웨어 체인

```
[HTTP Request]
     |
     v
+----+--------------------+
| SecurityHeadersMiddleware|  SECURITY-04: 보안 헤더 주입
+----+--------------------+
     |
     v
+----+--------------------+
| RequestIDMiddleware      |  요청 추적 ID 생성
+----+--------------------+
     |
     v
+----+--------------------+
| RateLimitMiddleware      |  SECURITY-11: Rate Limiting
+----+--------------------+
     |
     v
+----+--------------------+
| CORSMiddleware           |  SECURITY-08: CORS 정책
+----+--------------------+
     |
     v
+----+--------------------+
| Auth Dependency (DI)     |  SECURITY-08: JWT 검증 + RBAC
+----+--------------------+
     |
     v
+----+--------------------+
| Store Ownership Check    |  SECURITY-08: IDOR 방지
+----+--------------------+
     |
     v
[Router Handler]
```

### 2.2 RBAC 패턴 (Dependency Injection)

```python
# 패턴: FastAPI Depends 체인
async def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenPayload:
    """JWT 토큰 검증 → 사용자 정보 반환"""

async def require_owner(user: TokenPayload = Depends(get_current_user)) -> TokenPayload:
    """owner 역할 필수"""

async def require_admin(user: TokenPayload = Depends(get_current_user)) -> TokenPayload:
    """owner 또는 manager 역할 필수"""

async def require_table(token: str = Depends(oauth2_scheme)) -> TokenPayload:
    """table 역할 필수"""

# 라우터에서 사용
@router.post("/menus")
async def create_menu(
    data: MenuCreate,
    user: TokenPayload = Depends(require_owner),  # owner만
    service: MenuService = Depends(get_menu_service),
):
    ...
```

### 2.3 매장 소유권 검증 패턴

```python
# 패턴: URL store_id vs 토큰 store_id 비교
async def verify_store_access(
    store_id: int,  # URL 파라미터
    user: TokenPayload = Depends(get_current_user),
) -> int:
    if user.store_id != store_id:
        raise ForbiddenException("매장 접근 권한 없음")
    return store_id
```

---

## 3. 에러 처리 패턴: 커스텀 예외 계층

### 3.1 예외 클래스 계층

```
AppException (base)
  |
  +-- AuthException
  |     +-- InvalidCredentialsException (401)
  |     +-- TokenExpiredException (401)
  |     +-- InsufficientPermissionException (403)
  |     +-- AccountLockedException (423)
  |
  +-- NotFoundException (404)
  |     +-- OrderNotFoundException
  |     +-- MenuNotFoundException
  |     +-- TableNotFoundException
  |     +-- UserNotFoundException
  |
  +-- ConflictException (409)
  |     +-- DuplicateTableException
  |     +-- DuplicateUserException
  |     +-- DuplicateCategoryException
  |
  +-- ValidationException (400)
  |     +-- InvalidStatusTransitionException
  |     +-- InvalidMenuDataException
  |
  +-- BusinessRuleException (422)
  |     +-- PendingOrdersException
  |     +-- LastOwnerException
  |     +-- CannotDeleteSelfException
  |
  +-- RateLimitException (429)
```

### 3.2 글로벌 예외 핸들러 패턴

```python
# 패턴: FastAPI exception_handler
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    """비즈니스 예외 → 구조화된 에러 응답"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_code": exc.error_code,
            "message": exc.message,
            "details": exc.details,
        },
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """미처리 예외 → generic 500 응답 (SECURITY-09, SECURITY-15)"""
    logger.error("unhandled_exception", exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={
            "error_code": "GENERAL_INTERNAL_ERROR",
            "message": "서버 내부 오류가 발생했습니다.",
            "details": None,
        },
    )
```

---

## 4. SSE 이벤트 버스 패턴: 인메모리 asyncio.Queue

### 4.1 아키텍처

```
[OrderService]                    [SSEManager]
     |                                 |
     | publish(event)                  |
     v                                 |
+----+----+                    +-------+-------+
| EventBus |--- asyncio.Queue -->| Consumer    |
| (싱글턴)  |                    | (per store) |
+----------+                    +-------+-------+
                                       |
                               +-------+-------+
                               | broadcast()   |
                               +---+---+---+---+
                                   |   |   |
                              [conn1][conn2][conn3]
```

### 4.2 EventBus 패턴

```python
# 패턴: asyncio.Queue 기반 이벤트 버스
class EventBus:
    """매장별 이벤트 큐 관리"""
    _queues: Dict[int, asyncio.Queue]  # store_id → Queue

    async def publish(self, store_id: int, event: SSEEvent):
        """이벤트 발행 (non-blocking)"""

    async def subscribe(self, store_id: int) -> AsyncGenerator[SSEEvent, None]:
        """이벤트 구독 (SSE 연결당 1개)"""
```

### 4.3 SSEManager 패턴

```python
# 패턴: 연결 풀 + 이벤트 필터링
class SSEManager:
    _event_bus: EventBus
    _connections: Dict[int, Dict[str, List[SSEConnection]]]

    async def connect_admin(self, store_id: int) -> AsyncGenerator:
        """관리자 SSE 스트림 (매장 전체 이벤트)"""

    async def connect_table(self, store_id: int, table_id: int) -> AsyncGenerator:
        """테이블 SSE 스트림 (해당 테이블 이벤트만 필터)"""
```

### 4.4 서비스에서 이벤트 발행

```python
# 패턴: Service → EventBus 발행
class OrderService:
    def __init__(self, repo: OrderRepository, event_bus: EventBus):
        self._repo = repo
        self._event_bus = event_bus

    async def create_order(self, ...) -> Order:
        order = await self._repo.create(...)
        await self._event_bus.publish(
            store_id=order.store_id,
            event=SSEEvent(type="order_created", data=order)
        )
        return order
```

---

## 5. 관찰성 패턴: Request ID + 구조화 로깅

### 5.1 Request ID 전파 (contextvars)

```python
# 패턴: contextvars로 request_id 전파
import contextvars

request_id_var: contextvars.ContextVar[str] = contextvars.ContextVar("request_id")

class RequestIDMiddleware:
    async def dispatch(self, request: Request, call_next):
        rid = str(uuid.uuid4())
        request_id_var.set(rid)
        response = await call_next(request)
        response.headers["X-Request-ID"] = rid
        return response
```

### 5.2 structlog 설정 패턴

```python
# 패턴: structlog + request_id 자동 바인딩
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,  # request_id 자동 포함
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
)
```

### 5.3 로그 출력 예시

```json
{
  "timestamp": "2026-04-01T12:30:00.123Z",
  "level": "info",
  "request_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "event": "order_created",
  "store_id": 1,
  "order_id": 42,
  "order_no": "005"
}
```

---

## 6. 의존성 주입 패턴: FastAPI Depends 전체 활용

### 6.1 DI 체인 구조

```
[Router]
  |
  +-- Depends(get_db_session)        → AsyncSession
  +-- Depends(get_current_user)      → TokenPayload
  +-- Depends(verify_store_access)   → store_id
  +-- Depends(get_order_service)     → OrderService
       |
       +-- Depends(get_order_repo)   → OrderRepository
       +-- Depends(get_event_bus)    → EventBus
```

### 6.2 서비스 팩토리 패턴

```python
# 패턴: Depends 체인으로 서비스 인스턴스 생성
async def get_order_repository(db: AsyncSession = Depends(get_db_session)):
    return OrderRepository(db)

async def get_event_bus() -> EventBus:
    return event_bus_singleton

async def get_order_service(
    repo: OrderRepository = Depends(get_order_repository),
    event_bus: EventBus = Depends(get_event_bus),
) -> OrderService:
    return OrderService(repo=repo, event_bus=event_bus)
```

### 6.3 테스트 시 DI 오버라이드

```python
# 패턴: 테스트에서 의존성 교체
app.dependency_overrides[get_db_session] = lambda: mock_session
app.dependency_overrides[get_event_bus] = lambda: mock_event_bus
```

---

## 7. 신뢰성 패턴

### 7.1 트랜잭션 관리 패턴

```python
# 패턴: Service 레이어에서 트랜잭션 경계 관리
class OrderService:
    async def create_order(self, ...):
        async with self._repo.session.begin():  # 트랜잭션 시작
            order = await self._repo.create_order(...)
            items = await self._repo.create_order_items(...)
            # 트랜잭션 커밋 (자동)
        # 트랜잭션 외부에서 이벤트 발행
        await self._event_bus.publish(...)
```

### 7.2 DB 세션 관리 패턴

```python
# 패턴: async context manager로 세션 자동 정리
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

### 7.3 SSE 연결 정리 패턴

```python
# 패턴: disconnect 감지 시 자동 정리
async def sse_stream(request: Request, ...):
    connection = await sse_manager.connect(...)
    try:
        async for event in connection.stream():
            if await request.is_disconnected():
                break
            yield event
    finally:
        await sse_manager.disconnect(connection)
```

---

## 8. 성능 패턴

### 8.1 Async I/O 패턴
- 모든 DB 쿼리: SQLAlchemy async session
- 모든 외부 호출: httpx AsyncClient (boto3 제외)
- SSE: asyncio.Queue 기반 non-blocking 이벤트 전달

### 8.2 N+1 쿼리 방지 패턴

```python
# 패턴: selectinload로 관계 데이터 즉시 로딩
stmt = (
    select(Order)
    .options(selectinload(Order.items))
    .where(Order.store_id == store_id)
)
```

### 8.3 연결 풀 설정

```python
# 패턴: SQLAlchemy async 연결 풀
engine = create_async_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600,
    echo=False,  # 프로덕션에서 SQL 로깅 비활성화
)
```

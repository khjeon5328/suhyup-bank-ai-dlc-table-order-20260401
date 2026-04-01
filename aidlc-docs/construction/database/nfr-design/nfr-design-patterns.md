# NFR Design Patterns - Unit 1: database

---

## 1. Repository 패턴

### 1.1 구조
각 엔티티별 Repository 클래스를 정의하여 CRUD 로직을 캡슐화합니다.

```
Service Layer (backend 유닛)
    |
    v
Repository Layer (database 유닛)
    |
    v
SQLAlchemy Session → MySQL
```

### 1.2 Base Repository
모든 Repository가 상속하는 제네릭 Base Repository를 정의합니다.

```python
# 의사 코드 (Pseudo Code)
class BaseRepository[T]:
    - __init__(session: AsyncSession)
    - get_by_id(id) -> T | None
    - get_all(filters, skip, limit) -> list[T]
    - create(entity) -> T
    - update(entity, data) -> T
    - delete(id) -> bool
```

### 1.3 엔티티별 Repository

| Repository | 엔티티 | 추가 메서드 |
|-----------|--------|------------|
| StoreRepository | Store | get_by_code(store_code) |
| UserRepository | User | get_by_username(store_code, username), get_active_users(store_code) |
| TableRepository | RestaurantTable | get_by_table_no(store_code, table_no) |
| SessionRepository | TableSession | get_active_session(store_code, table_no), end_session(session_id) |
| CategoryRepository | Category | get_by_store(store_code, ordered=True) |
| MenuRepository | Menu | get_by_category(store_code, category_id), update_sort_orders(menu_orders) |
| OrderRepository | Order | get_current_orders(store_code), get_archived_orders(store_code, table_no, date_from, date_to), archive_by_session(session_id) |
| OrderItemRepository | OrderItem | get_by_order(order_id) |

### 1.4 소프트 삭제 Repository
Menu, User Repository는 기본 쿼리에 `deleted_at IS NULL` 필터가 자동 적용됩니다.
삭제된 데이터 포함 조회가 필요한 경우 `include_deleted=True` 파라미터로 필터 해제.

---

## 2. Mixin 패턴

### 2.1 TimestampMixin
모든 모델에 적용되는 공통 타임스탬프 필드.

```python
# 의사 코드
class TimestampMixin:
    created_at: datetime  # server_default=func.now()
    updated_at: datetime  # server_default=func.now(), onupdate=func.now()
```

**적용 대상**: Store, User, RestaurantTable, TableSession, Category, Menu, Order, OrderItem(created_at만)

### 2.2 SoftDeleteMixin
선택적으로 적용되는 소프트 삭제 필드 + 자동 필터.

```python
# 의사 코드
class SoftDeleteMixin:
    deleted_at: datetime | None  # nullable, default=None

    # 소프트 삭제 실행
    def soft_delete() -> None:
        self.deleted_at = func.now()

    # 복원
    def restore() -> None:
        self.deleted_at = None
```

**적용 대상**: Menu, User
**자동 필터**: Repository의 기본 쿼리에 `.where(Model.deleted_at.is_(None))` 자동 적용

---

## 3. 트랜잭션 관리 패턴

### 3.1 세션 스코프
- FastAPI 요청별 세션 생성 (Dependency Injection)
- `async with` 컨텍스트 매니저로 세션 라이프사이클 관리
- 요청 완료 시 자동 커밋 또는 롤백

### 3.2 복합 트랜잭션
여러 Repository를 사용하는 비즈니스 로직은 단일 세션(트랜잭션)으로 처리.

**예시: 이용 완료 처리**
```
1개 트랜잭션:
  1. SessionRepository.end_session(session_id)     # 세션 종료
  2. OrderRepository.archive_by_session(session_id) # 주문 아카이브
  3. commit
  실패 시 → 자동 rollback
```

### 3.3 에러 처리
- DB 연결 실패: ConnectionError → 503 Service Unavailable
- 제약조건 위반: IntegrityError → 400 Bad Request (상세 메시지는 내부 로그만)
- 타임아웃: TimeoutError → 504 Gateway Timeout
- 모든 예외에서 트랜잭션 자동 롤백

---

## 4. 보안 패턴

### 4.1 비밀번호 해싱
```python
# 의사 코드
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
```

**적용 위치**: database/utils/security.py (database 유닛에서 제공, backend 유닛에서 import)

### 4.2 민감 데이터 보호
- Pydantic Response 스키마에서 `password_hash` 필드 제외 (`model_config`의 `exclude` 또는 별도 Response 모델)
- `__repr__` 메서드에서 비밀번호 필드 마스킹

---

## 5. 설정 관리 패턴

### 5.1 Pydantic Settings
```python
# 의사 코드
class DatabaseSettings(BaseSettings):
    db_host: str = "localhost"
    db_port: int = 3306
    db_user: str = "tableorder"
    db_password: str  # 필수, 기본값 없음
    db_name: str = "tableorder"
    db_pool_size: int = 10
    db_max_overflow: int = 20
    db_echo: bool = False
    db_ssl_mode: str | None = None
    environment: str = "development"

    model_config = SettingsConfigDict(env_file=".env")
```

### 5.2 환경별 분기
- `environment == "production"`: TLS 필수, echo=False
- `environment == "development"`: TLS 선택, echo 설정 가능
- `environment == "test"`: 테스트 DB 사용, echo=True

---

## 6. 커넥션 풀 관리 패턴

### 6.1 엔진 설정
```python
# 의사 코드
engine = create_async_engine(
    url=database_url,
    pool_size=settings.db_pool_size,       # 10
    max_overflow=settings.db_max_overflow,  # 20
    pool_timeout=30,
    pool_recycle=3600,
    pool_pre_ping=True,
    echo=settings.db_echo,
)
```

### 6.2 세션 팩토리
```python
# 의사 코드
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
```

### 6.3 Dependency Injection
```python
# 의사 코드
async def get_db_session() -> AsyncGenerator[AsyncSession]:
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

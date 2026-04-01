# Code Summary - Unit 1: database

## 생성된 파일 목록

### 설정 (3개)
- `table-order/database/config.py` — DatabaseSettings (Pydantic Settings)
- `table-order/database/database.py` — 엔진, 세션 팩토리, DI
- `table-order/database/.env.example` — 환경 변수 템플릿

### 모델 (8개)
- `models/base.py` — Base, TimestampMixin, SoftDeleteMixin
- `models/store.py` — Store (VARCHAR PK)
- `models/user.py` — User (SoftDeleteMixin, UserRole Enum)
- `models/table.py` — RestaurantTable (복합 PK)
- `models/session.py` — TableSession (시간 기반 상태)
- `models/category.py` — Category (매장별 고유)
- `models/menu.py` — Menu (SoftDeleteMixin, CHECK 제약)
- `models/order.py` — Order + OrderItem (아카이브, 스냅샷)

### 스키마 (10개)
- `schemas/common.py` — PaginationParams, PaginatedResponse, ErrorResponse
- `schemas/store.py` — StoreBase, StoreCreate, StoreResponse
- `schemas/user.py` — UserBase, UserCreate, UserUpdate, UserResponse
- `schemas/table.py` — TableCreate, TableResponse
- `schemas/session.py` — SessionResponse
- `schemas/category.py` — CategoryBase, CategoryCreate, CategoryUpdate, CategoryResponse
- `schemas/menu.py` — MenuBase, MenuCreate, MenuUpdate, MenuResponse, MenuOrderUpdate
- `schemas/order.py` — OrderItemCreate, OrderCreate, OrderItemResponse, OrderResponse, OrderStatusUpdate
- `schemas/auth.py` — AdminLoginRequest, TableLoginRequest, TokenResponse

### Repository (8개)
- `repositories/base.py` — BaseRepository[T] (제네릭 CRUD)
- `repositories/store.py` — StoreRepository
- `repositories/user.py` — UserRepository (소프트 삭제)
- `repositories/table.py` — TableRepository
- `repositories/session.py` — SessionRepository (세션 라이프사이클)
- `repositories/category.py` — CategoryRepository
- `repositories/menu.py` — MenuRepository (소프트 삭제)
- `repositories/order.py` — OrderRepository (아카이브)

### 유틸리티 (1개)
- `utils/security.py` — hash_password, verify_password (passlib bcrypt)

### 마이그레이션 (3개)
- `alembic.ini` — Alembic 설정
- `alembic/env.py` — 마이그레이션 환경
- `alembic/versions/001_initial_schema.py` — 초기 스키마 (8개 테이블)

### 시드 데이터 (3개)
- `seed/seed_data.py` — 매장, 사용자, 테이블, 카테고리 데이터
- `seed/menus.py` — 메뉴 데이터 (매장당 8개)
- `seed/run_seed.py` — 시드 실행 스크립트 (멱등성)

### 테스트 (4개)
- `tests/conftest.py` — 테스트 DB 설정, 세션 fixture
- `tests/test_models.py` — 모델 CRUD, 제약조건, 관계 (7개 테스트)
- `tests/test_schemas.py` — 스키마 검증 (14개 테스트)
- `tests/test_repositories.py` — Repository CRUD, 소프트 삭제, 아카이브 (5개 테스트)
- `tests/test_security.py` — 해싱/검증 (5개 테스트)

## 총 파일 수: 약 43개

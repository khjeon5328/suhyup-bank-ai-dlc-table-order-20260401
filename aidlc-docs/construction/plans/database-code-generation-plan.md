# Code Generation Plan - Unit 1: database

## 유닛 컨텍스트
- **유닛명**: database
- **프로젝트 타입**: Greenfield, Multi-unit
- **코드 위치**: `table-order/database/` (워크스페이스 루트 기준)
- **기술 스택**: Python 3.11+, SQLAlchemy 2.0+, Alembic, Pydantic 2.0+, passlib[bcrypt], pydantic-settings, asyncmy
- **의존 유닛**: 없음 (기반 유닛)
- **의존하는 유닛**: backend (models, schemas, repositories, config, utils import)

## 스토리 커버리지
database 유닛은 모든 23개 스토리의 데이터 모델 기반을 제공합니다.
- US-C01~C08: 고객 스토리 (Table, TableSession, Menu, Category, Order, OrderItem)
- US-O01~O11: 점주 스토리 (Store, User, 전체 모델)
- US-M01~M04: 매니저 스토리 (User role 기반)

## 코드 생성 단계

### Step 1: 프로젝트 구조 및 설정 파일
- [x] `table-order/database/` 디렉토리 구조 생성
- [x] `requirements.txt` 생성 (의존성 핀닝)
- [x] `config.py` 생성 (DatabaseSettings - Pydantic Settings)
- [x] `database.py` 생성 (엔진, 세션 팩토리, DI)
- [x] `.env.example` 생성 (환경 변수 템플릿)

### Step 2: 모델 기반 (Base, Mixin)
- [x] `models/__init__.py` 생성
- [x] `models/base.py` 생성 (Base, TimestampMixin, SoftDeleteMixin)

### Step 3: 엔티티 모델
- [x] `models/store.py` 생성 (Store)
- [x] `models/user.py` 생성 (User - SoftDeleteMixin 적용)
- [x] `models/table.py` 생성 (RestaurantTable - 복합 PK)
- [x] `models/session.py` 생성 (TableSession)
- [x] `models/category.py` 생성 (Category)
- [x] `models/menu.py` 생성 (Menu - SoftDeleteMixin 적용)
- [x] `models/order.py` 생성 (Order, OrderItem)

### Step 4: Pydantic 스키마
- [x] `schemas/__init__.py` 생성
- [x] `schemas/common.py` 생성 (PaginationParams, PaginatedResponse, ErrorResponse)
- [x] `schemas/store.py` 생성 (StoreBase, StoreCreate, StoreResponse)
- [x] `schemas/user.py` 생성 (UserBase, UserCreate, UserUpdate, UserResponse)
- [x] `schemas/table.py` 생성 (TableCreate, TableResponse)
- [x] `schemas/session.py` 생성 (SessionResponse)
- [x] `schemas/category.py` 생성 (CategoryBase, CategoryCreate, CategoryUpdate, CategoryResponse)
- [x] `schemas/menu.py` 생성 (MenuBase, MenuCreate, MenuUpdate, MenuResponse, MenuOrderUpdate)
- [x] `schemas/order.py` 생성 (OrderItemCreate, OrderCreate, OrderItemResponse, OrderResponse, OrderStatusUpdate)
- [x] `schemas/auth.py` 생성 (AdminLoginRequest, TableLoginRequest, TokenResponse)

### Step 5: Repository 레이어
- [x] `repositories/__init__.py` 생성
- [x] `repositories/base.py` 생성 (BaseRepository[T])
- [x] `repositories/store.py` 생성 (StoreRepository)
- [x] `repositories/user.py` 생성 (UserRepository - 소프트 삭제 필터)
- [x] `repositories/table.py` 생성 (TableRepository)
- [x] `repositories/session.py` 생성 (SessionRepository)
- [x] `repositories/category.py` 생성 (CategoryRepository)
- [x] `repositories/menu.py` 생성 (MenuRepository - 소프트 삭제 필터)
- [x] `repositories/order.py` 생성 (OrderRepository - 아카이브 로직)

### Step 6: 보안 유틸리티
- [x] `utils/__init__.py` 생성
- [x] `utils/security.py` 생성 (CryptContext, hash_password, verify_password)

### Step 7: Alembic 마이그레이션 설정
- [x] `alembic.ini` 생성
- [x] `alembic/env.py` 생성 (비동기 마이그레이션 설정)
- [x] `alembic/script.py.mako` 생성
- [x] 초기 마이그레이션 파일 생성 (전체 스키마)

### Step 8: 시드 데이터
- [x] `seed/__init__.py` 생성
- [x] `seed/seed_data.py` 생성 (시드 데이터 정의)
- [x] `seed/run_seed.py` 생성 (시드 실행 스크립트)

### Step 9: 단위 테스트
- [x] `tests/__init__.py` 생성
- [x] `tests/conftest.py` 생성 (테스트 DB 설정, 세션 fixture)
- [x] `tests/test_models.py` 생성 (모델 CRUD, 제약조건, 관계 테스트)
- [x] `tests/test_schemas.py` 생성 (스키마 검증 테스트)
- [x] `tests/test_repositories.py` 생성 (Repository CRUD, 소프트 삭제, 아카이브 테스트)
- [x] `tests/test_security.py` 생성 (해싱/검증 테스트)

### Step 10: 문서 및 마무리
- [x] `aidlc-docs/construction/database/code/code-summary.md` 생성 (코드 요약)
- [x] 전체 체크박스 완료 확인

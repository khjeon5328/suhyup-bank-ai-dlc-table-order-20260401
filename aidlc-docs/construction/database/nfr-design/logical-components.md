# Logical Components - Unit 1: database

---

## 컴포넌트 구조도

```
database/
+-----------------------------------------------+
|                                               |
|  +-- models/                                  |
|  |   +-- base.py                              |
|  |   |   +-- Base (DeclarativeBase)           |
|  |   |   +-- TimestampMixin                   |
|  |   |   +-- SoftDeleteMixin                  |
|  |   +-- store.py      (Store)                |
|  |   +-- user.py        (User)                |
|  |   +-- table.py       (RestaurantTable)     |
|  |   +-- session.py     (TableSession)        |
|  |   +-- category.py    (Category)            |
|  |   +-- menu.py        (Menu)                |
|  |   +-- order.py       (Order, OrderItem)    |
|  |                                            |
|  +-- schemas/                                 |
|  |   +-- store.py       (Store DTOs)          |
|  |   +-- user.py        (User DTOs)           |
|  |   +-- table.py       (Table DTOs)          |
|  |   +-- session.py     (Session DTOs)        |
|  |   +-- category.py    (Category DTOs)       |
|  |   +-- menu.py        (Menu DTOs)           |
|  |   +-- order.py       (Order DTOs)          |
|  |   +-- auth.py        (Auth DTOs)           |
|  |   +-- common.py      (Pagination 등)       |
|  |                                            |
|  +-- repositories/                            |
|  |   +-- base.py        (BaseRepository[T])   |
|  |   +-- store.py       (StoreRepository)     |
|  |   +-- user.py        (UserRepository)      |
|  |   +-- table.py       (TableRepository)     |
|  |   +-- session.py     (SessionRepository)   |
|  |   +-- category.py    (CategoryRepository)  |
|  |   +-- menu.py        (MenuRepository)      |
|  |   +-- order.py       (OrderRepository)     |
|  |                                            |
|  +-- seed/                                    |
|  |   +-- seed_data.py   (시드 데이터 정의)    |
|  |   +-- run_seed.py    (시드 실행 스크립트)  |
|  |                                            |
|  +-- utils/                                   |
|  |   +-- security.py    (해싱 유틸리티)       |
|  |                                            |
|  +-- alembic/                                 |
|  |   +-- env.py                               |
|  |   +-- versions/                            |
|  |                                            |
|  +-- alembic.ini                              |
|  +-- database.py        (엔진, 세션, DI)      |
|  +-- config.py          (DatabaseSettings)    |
|  +-- requirements.txt                         |
|                                               |
+-----------------------------------------------+
```

---

## 컴포넌트 상세

### 1. models/ — SQLAlchemy ORM 모델

| 파일 | 클래스 | Mixin | 설명 |
|------|--------|-------|------|
| base.py | Base, TimestampMixin, SoftDeleteMixin | - | 공통 기반 |
| store.py | Store | TimestampMixin | 매장 |
| user.py | User | TimestampMixin, SoftDeleteMixin | 관리자 계정 |
| table.py | RestaurantTable | TimestampMixin | 테이블 |
| session.py | TableSession | - | 테이블 세션 (created_at만) |
| category.py | Category | TimestampMixin | 메뉴 카테고리 |
| menu.py | Menu | TimestampMixin, SoftDeleteMixin | 메뉴 |
| order.py | Order, OrderItem | TimestampMixin / created_at만 | 주문, 주문 항목 |

### 2. schemas/ — Pydantic DTO

각 엔티티별 Base, Create, Update, Response 스키마 제공.
- `common.py`: PaginationParams, PaginatedResponse[T], ErrorResponse
- `auth.py`: AdminLoginRequest, TableLoginRequest, TokenResponse

### 3. repositories/ — 데이터 접근 계층

| 파일 | 클래스 | 소프트 삭제 자동 필터 |
|------|--------|---------------------|
| base.py | BaseRepository[T] | 선택적 |
| store.py | StoreRepository | N/A |
| user.py | UserRepository | ✅ |
| table.py | TableRepository | N/A |
| session.py | SessionRepository | N/A |
| category.py | CategoryRepository | N/A |
| menu.py | MenuRepository | ✅ |
| order.py | OrderRepository | N/A (archived_at는 별도 로직) |

### 4. 인프라 컴포넌트

| 파일 | 역할 | 주요 내용 |
|------|------|----------|
| database.py | DB 엔진/세션 관리 | create_async_engine, async_sessionmaker, get_db_session DI |
| config.py | 설정 관리 | DatabaseSettings (Pydantic Settings) |
| utils/security.py | 보안 유틸리티 | CryptContext, hash_password, verify_password |

### 5. 마이그레이션/시드

| 파일 | 역할 |
|------|------|
| alembic/ | Alembic 마이그레이션 설정 및 버전 파일 |
| seed/seed_data.py | 시드 데이터 정의 (매장 2개, 관리자 4명, 테이블 10개, 카테고리 8개, 메뉴 16개) |
| seed/run_seed.py | 시드 실행 스크립트 (멱등성 보장) |

---

## 의존성 흐름

```
backend 유닛 (Service Layer)
    |
    | import
    v
database 유닛
    +-- repositories/  <-- Service가 직접 사용
    +-- schemas/       <-- API 요청/응답 DTO
    +-- models/        <-- Repository가 내부 사용
    +-- database.py    <-- 세션 DI 제공
    +-- config.py      <-- 설정 제공
    +-- utils/         <-- 보안 유틸리티 제공
```

---

## 패키지 의존성 (requirements.txt)

```
sqlalchemy>=2.0,<3.0
alembic>=1.13,<2.0
asyncmy>=0.2,<1.0
pydantic>=2.0,<3.0
pydantic-settings>=2.0,<3.0
passlib[bcrypt]>=1.7,<2.0
```

### 테스트 의존성
```
pytest>=8.0,<9.0
pytest-asyncio>=0.23,<1.0
```

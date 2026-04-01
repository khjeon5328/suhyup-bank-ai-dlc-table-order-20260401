# Business Logic Model - Unit 1: database

---

## 1. 시드 데이터 전략

### 1.1 시드 데이터 범위 (중간 규모)

| 엔티티 | 수량 | 상세 |
|--------|------|------|
| Store | 2개 | PIZZA01 (피자매장), CHICKEN01 (치킨매장) |
| User | 4명 | 매장당 점주 1명 + 매니저 1명 |
| RestaurantTable | 매장당 5개 | 테이블 1~5번 |
| Category | 매장당 4개 | 예: 메인, 사이드, 음료, 디저트 |
| Menu | 매장당 8개 | 카테고리별 2개씩 |

### 1.2 시드 데이터 상세

**매장 1: PIZZA01**
- 점주: admin / password123
- 매니저: manager1 / password123
- 카테고리: 피자, 파스타, 음료, 디저트
- 메뉴: 카테고리별 2개 (총 8개)

**매장 2: CHICKEN01**
- 점주: admin / password123
- 매니저: manager1 / password123
- 카테고리: 치킨, 사이드, 음료, 세트메뉴
- 메뉴: 카테고리별 2개 (총 8개)

### 1.3 시드 실행 규칙
- Alembic 마이그레이션 후 별도 시드 스크립트로 실행
- 멱등성 보장: Store 테이블에 데이터가 있으면 건너뜀
- 비밀번호는 bcrypt 해싱 적용
- 테이블 PIN은 "1234" (4자리) 기본값

---

## 2. 마이그레이션 전략

### 2.1 Alembic 설정
- 비동기 SQLAlchemy 엔진 사용
- 마이그레이션 디렉토리: `database/alembic/`
- 초기 마이그레이션: 전체 스키마 생성 (1개 파일)

### 2.2 마이그레이션 순서
1. Store 테이블 생성
2. User 테이블 생성 (FK: store_code)
3. RestaurantTable 테이블 생성 (FK: store_code)
4. TableSession 테이블 생성 (FK: store_code, table_no)
5. Category 테이블 생성 (FK: store_code)
6. Menu 테이블 생성 (FK: store_code, category_id)
7. Order 테이블 생성 (FK: store_code, session_id)
8. OrderItem 테이블 생성 (FK: order_id, menu_id)

### 2.3 인덱스 전략
- PK: 모든 테이블에 기본 적용
- FK: 외래 키 필드에 자동 인덱스
- 복합 인덱스: 자주 사용되는 쿼리 패턴 기반
  - `(store_code, table_no, ended_at)` — 활성 세션 조회
  - `(store_code, archived_at, created_at)` — 현재/과거 주문 조회
  - `(store_code, category_id, sort_order)` — 메뉴 목록 조회

---

## 3. DB 연결 설정 패턴

### 3.1 비동기 연결
- SQLAlchemy 2.0 async 엔진 사용
- `asyncmy` MySQL 비동기 드라이버
- 커넥션 풀: pool_size=10, max_overflow=20

### 3.2 연결 문자열 구조
```
mysql+asyncmy://{user}:{password}@{host}:{port}/{database}
```

### 3.3 세션 관리
- `async_sessionmaker`로 세션 팩토리 생성
- FastAPI Dependency Injection으로 요청별 세션 제공
- 요청 완료 시 자동 세션 종료 (async context manager)

---

## 4. Pydantic 스키마 구조

### 4.1 스키마 분류 체계

각 엔티티별로 다음 스키마를 정의:
- **Base**: 공통 필드 (입력/출력 공유)
- **Create**: 생성 요청 DTO
- **Update**: 수정 요청 DTO (모든 필드 Optional)
- **Response**: API 응답 DTO (id, timestamps 포함)

### 4.2 엔티티별 스키마

**Store**
- `StoreBase`: name, address?, phone?
- `StoreCreate`: StoreBase + store_code
- `StoreResponse`: StoreBase + store_code, created_at, updated_at

**User**
- `UserBase`: username, role
- `UserCreate`: UserBase + password
- `UserUpdate`: username?, role?, password? (모두 Optional)
- `UserResponse`: UserBase + id, store_code, created_at, updated_at

**RestaurantTable**
- `TableCreate`: table_no, password (PIN)
- `TableResponse`: store_code, table_no, created_at, updated_at

**TableSession**
- `SessionResponse`: id, store_code, table_no, started_at, ended_at

**Category**
- `CategoryBase`: name, sort_order?
- `CategoryCreate`: CategoryBase
- `CategoryUpdate`: name?, sort_order?
- `CategoryResponse`: CategoryBase + id, store_code, created_at, updated_at

**Menu**
- `MenuBase`: name, price, description?, category_id, image_url?, sort_order?
- `MenuCreate`: MenuBase
- `MenuUpdate`: name?, price?, description?, category_id?, image_url?, sort_order?
- `MenuResponse`: MenuBase + id, store_code, created_at, updated_at
- `MenuOrderUpdate`: List[{menu_id, sort_order}]

**Order**
- `OrderItemCreate`: menu_id, quantity
- `OrderCreate`: items (List[OrderItemCreate])
- `OrderItemResponse`: id, menu_id, menu_name, quantity, unit_price, subtotal
- `OrderResponse`: id, store_code, table_no, session_id, total_amount, status, items, created_at, updated_at
- `OrderStatusUpdate`: status

**Auth**
- `AdminLoginRequest`: store_code, username, password
- `TableLoginRequest`: store_code, table_no, password
- `TokenResponse`: access_token, token_type

### 4.3 공통 스키마
- `PaginationParams`: page (default=1), page_size (default=20)
- `PaginatedResponse[T]`: items, total, page, page_size, total_pages
- `ErrorResponse`: detail (str)

---

## 5. 코드 조직 구조

```
database/
+-- models/
|   +-- __init__.py
|   +-- base.py          # Base, TimestampMixin
|   +-- store.py          # Store 모델
|   +-- user.py           # User 모델
|   +-- table.py          # RestaurantTable 모델
|   +-- session.py        # TableSession 모델
|   +-- category.py       # Category 모델
|   +-- menu.py           # Menu 모델
|   +-- order.py          # Order, OrderItem 모델
+-- schemas/
|   +-- __init__.py
|   +-- store.py          # Store 스키마
|   +-- user.py           # User 스키마
|   +-- table.py          # Table 스키마
|   +-- session.py        # Session 스키마
|   +-- category.py       # Category 스키마
|   +-- menu.py           # Menu 스키마
|   +-- order.py          # Order, OrderItem 스키마
|   +-- auth.py           # Auth 스키마
|   +-- common.py         # 공통 스키마 (Pagination 등)
+-- seed/
|   +-- __init__.py
|   +-- seed_data.py      # 시드 데이터 정의
|   +-- run_seed.py       # 시드 실행 스크립트
+-- alembic/
|   +-- env.py
|   +-- versions/         # 마이그레이션 파일
+-- alembic.ini
+-- database.py           # DB 연결 설정 (엔진, 세션)
+-- requirements.txt
```

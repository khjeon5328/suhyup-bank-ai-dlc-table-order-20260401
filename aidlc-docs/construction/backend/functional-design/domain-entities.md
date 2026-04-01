# Backend - 도메인 엔티티 설계

---

## 1. 엔티티 관계 다이어그램

```
+----------+       +----------+       +----------------+
|  Store   |1----*|   User   |       | TableSession   |
|----------|       |----------|       |----------------|
| id (PK)  |       | id (PK)  |       | id (PK)        |
| name     |       | store_id |       | store_id (FK)  |
| code     |       | username |       | table_id (FK)  |
| address  |       | password |       | started_at     |
| phone    |       | role     |       | ended_at       |
| is_active|       | is_active|       | is_active      |
| created  |       | created  |       | created_at     |
| updated  |       | updated  |       +-------+--------+
+----+-----+       +----------+               |
     |                                         |
     |1                                        |*
     |                                         |
     |*                                        |
+----+-----+       +----------+       +-------+--------+
|  Table   |1----*|  Order   |*----1| TableSession   |
|----------|       |----------|       +----------------+
| id (PK)  |       | id (PK)  |
| store_id |       | store_id |
| table_no |       | table_id |
| password |       | session_id|
| is_active|       | order_no |
| created  |       | total    |
| updated  |       | status   |
+----+-----+       | is_deleted|
     |              | created  |
     |              | updated  |
     |              +----+-----+
     |                   |
     |                   |*
     |              +----+------+
     |              | OrderItem |
     |              |-----------|
     |              | id (PK)   |
     |              | order_id  |
     |              | menu_id   |
     |              | menu_name |
     |              | quantity  |
     |              | unit_price|
     |              | subtotal  |
     |              +-----------+
     |
+----+-----+
| Category |1----*+----------+
|----------|       |   Menu   |
| id (PK)  |       |----------|
| store_id |       | id (PK)  |
| name     |       | store_id |
| sort_order|      | category_id|
| is_active|       | name     |
| created  |       | price    |
| updated  |       | description|
+----------+       | image_url|
                   | sort_order|
                   | is_active|
                   | created  |
                   | updated  |
                   +----------+

+----------------+
| OrderHistory   |
|----------------|
| id (PK)        |
| store_id (FK)  |
| table_id (FK)  |
| session_id(FK) |
| order_id (원본)|
| order_no       |
| order_data(JSON)|
| total          |
| status         |
| ordered_at     |
| archived_at    |
+----------------+

+------------------+
| LoginAttempt     |
|------------------|
| id (PK)          |
| store_id         |
| username         |
| ip_address       |
| success          |
| attempted_at     |
+------------------+
```

---

## 2. 엔티티 상세 정의

### 2.1 Store (매장)

| 필드 | 타입 | 제약조건 | 설명 |
|------|------|---------|------|
| id | Integer | PK, Auto Increment | 매장 고유 ID |
| name | String(100) | NOT NULL | 매장명 |
| code | String(50) | NOT NULL, UNIQUE | 매장 식별 코드 (로그인용) |
| address | String(255) | NULL | 매장 주소 |
| phone | String(20) | NULL | 매장 전화번호 |
| is_active | Boolean | NOT NULL, DEFAULT true | 활성 상태 |
| created_at | DateTime | NOT NULL, DEFAULT now | 생성 시각 |
| updated_at | DateTime | NOT NULL, DEFAULT now | 수정 시각 |

**관계**: Store 1 → * Table, Store 1 → * User, Store 1 → * Category, Store 1 → * Menu, Store 1 → * Order

---

### 2.2 User (관리자 계정)

| 필드 | 타입 | 제약조건 | 설명 |
|------|------|---------|------|
| id | Integer | PK, Auto Increment | 사용자 고유 ID |
| store_id | Integer | FK(Store), NOT NULL | 소속 매장 |
| username | String(50) | NOT NULL | 사용자명 |
| password_hash | String(255) | NOT NULL | bcrypt 해시 비밀번호 |
| role | Enum(owner, manager) | NOT NULL | 역할 |
| is_active | Boolean | NOT NULL, DEFAULT true | 활성 상태 |
| created_at | DateTime | NOT NULL, DEFAULT now | 생성 시각 |
| updated_at | DateTime | NOT NULL, DEFAULT now | 수정 시각 |

**제약**: UNIQUE(store_id, username)
**관계**: User * → 1 Store

---

### 2.3 Table (테이블)

| 필드 | 타입 | 제약조건 | 설명 |
|------|------|---------|------|
| id | Integer | PK, Auto Increment | 테이블 고유 ID |
| store_id | Integer | FK(Store), NOT NULL | 소속 매장 |
| table_no | Integer | NOT NULL | 테이블 번호 |
| password_hash | String(255) | NOT NULL | bcrypt 해시 비밀번호 |
| is_active | Boolean | NOT NULL, DEFAULT true | 활성 상태 |
| created_at | DateTime | NOT NULL, DEFAULT now | 생성 시각 |
| updated_at | DateTime | NOT NULL, DEFAULT now | 수정 시각 |

**제약**: UNIQUE(store_id, table_no)
**관계**: Table * → 1 Store, Table 1 → * TableSession, Table 1 → * Order

---

### 2.4 TableSession (테이블 세션)

| 필드 | 타입 | 제약조건 | 설명 |
|------|------|---------|------|
| id | Integer | PK, Auto Increment | 세션 고유 ID |
| store_id | Integer | FK(Store), NOT NULL | 소속 매장 |
| table_id | Integer | FK(Table), NOT NULL | 테이블 |
| started_at | DateTime | NOT NULL, DEFAULT now | 세션 시작 시각 |
| ended_at | DateTime | NULL | 세션 종료 시각 (이용 완료 시) |
| is_active | Boolean | NOT NULL, DEFAULT true | 활성 상태 |
| created_at | DateTime | NOT NULL, DEFAULT now | 생성 시각 |

**관계**: TableSession * → 1 Table, TableSession 1 → * Order
**비즈니스 규칙**: 테이블당 활성 세션은 최대 1개

---

### 2.5 Category (메뉴 카테고리)

| 필드 | 타입 | 제약조건 | 설명 |
|------|------|---------|------|
| id | Integer | PK, Auto Increment | 카테고리 고유 ID |
| store_id | Integer | FK(Store), NOT NULL | 소속 매장 |
| name | String(50) | NOT NULL | 카테고리명 |
| sort_order | Integer | NOT NULL, DEFAULT 0 | 노출 순서 |
| is_active | Boolean | NOT NULL, DEFAULT true | 활성 상태 |
| created_at | DateTime | NOT NULL, DEFAULT now | 생성 시각 |
| updated_at | DateTime | NOT NULL, DEFAULT now | 수정 시각 |

**제약**: UNIQUE(store_id, name)
**관계**: Category * → 1 Store, Category 1 → * Menu

---

### 2.6 Menu (메뉴)

| 필드 | 타입 | 제약조건 | 설명 |
|------|------|---------|------|
| id | Integer | PK, Auto Increment | 메뉴 고유 ID |
| store_id | Integer | FK(Store), NOT NULL | 소속 매장 |
| category_id | Integer | FK(Category), NOT NULL | 카테고리 |
| name | String(100) | NOT NULL | 메뉴명 |
| price | Integer | NOT NULL, CHECK >= 0 | 가격 (원) |
| description | Text | NULL | 메뉴 설명 |
| image_url | String(500) | NULL | 이미지 URL |
| sort_order | Integer | NOT NULL, DEFAULT 0 | 노출 순서 |
| is_active | Boolean | NOT NULL, DEFAULT true | 활성 상태 |
| created_at | DateTime | NOT NULL, DEFAULT now | 생성 시각 |
| updated_at | DateTime | NOT NULL, DEFAULT now | 수정 시각 |

**관계**: Menu * → 1 Store, Menu * → 1 Category

---

### 2.7 Order (주문)

| 필드 | 타입 | 제약조건 | 설명 |
|------|------|---------|------|
| id | Integer | PK, Auto Increment | 주문 고유 ID |
| store_id | Integer | FK(Store), NOT NULL | 소속 매장 |
| table_id | Integer | FK(Table), NOT NULL | 테이블 |
| session_id | Integer | FK(TableSession), NOT NULL | 세션 |
| order_no | String(10) | NOT NULL | 매장별 일일 순번 (예: "001") |
| total_amount | Integer | NOT NULL, CHECK >= 0 | 총 주문 금액 (원) |
| status | Enum(pending, preparing, completed) | NOT NULL, DEFAULT pending | 주문 상태 |
| is_deleted | Boolean | NOT NULL, DEFAULT false | 논리적 삭제 플래그 |
| deleted_at | DateTime | NULL | 삭제 시각 |
| created_at | DateTime | NOT NULL, DEFAULT now | 주문 시각 |
| updated_at | DateTime | NOT NULL, DEFAULT now | 수정 시각 |

**제약**: UNIQUE(store_id, order_no, DATE(created_at)) — 매장별 일일 순번 유니크
**관계**: Order * → 1 Store, Order * → 1 Table, Order * → 1 TableSession, Order 1 → * OrderItem

---

### 2.8 OrderItem (주문 항목)

| 필드 | 타입 | 제약조건 | 설명 |
|------|------|---------|------|
| id | Integer | PK, Auto Increment | 항목 고유 ID |
| order_id | Integer | FK(Order), NOT NULL | 주문 |
| menu_id | Integer | FK(Menu), NOT NULL | 메뉴 |
| menu_name | String(100) | NOT NULL | 주문 시점 메뉴명 (스냅샷) |
| quantity | Integer | NOT NULL, CHECK >= 1 | 수량 |
| unit_price | Integer | NOT NULL, CHECK >= 0 | 주문 시점 단가 (스냅샷) |
| subtotal | Integer | NOT NULL, CHECK >= 0 | 소계 (quantity * unit_price) |

**관계**: OrderItem * → 1 Order, OrderItem * → 1 Menu

---

### 2.9 OrderHistory (주문 아카이브)

| 필드 | 타입 | 제약조건 | 설명 |
|------|------|---------|------|
| id | Integer | PK, Auto Increment | 이력 고유 ID |
| store_id | Integer | FK(Store), NOT NULL | 소속 매장 |
| table_id | Integer | FK(Table), NOT NULL | 테이블 |
| session_id | Integer | FK(TableSession), NOT NULL | 세션 |
| original_order_id | Integer | NOT NULL | 원본 주문 ID |
| order_no | String(10) | NOT NULL | 주문 번호 |
| order_data | JSON | NOT NULL | 주문 상세 (메뉴 목록, 수량, 단가 등) |
| total_amount | Integer | NOT NULL | 총 금액 |
| status | String(20) | NOT NULL | 아카이브 시점 상태 |
| ordered_at | DateTime | NOT NULL | 원본 주문 시각 |
| archived_at | DateTime | NOT NULL, DEFAULT now | 아카이브 시각 |

**관계**: OrderHistory * → 1 Store, OrderHistory * → 1 Table

---

### 2.10 LoginAttempt (로그인 시도 기록)

| 필드 | 타입 | 제약조건 | 설명 |
|------|------|---------|------|
| id | Integer | PK, Auto Increment | 기록 고유 ID |
| store_id | Integer | NULL | 매장 ID (입력된 경우) |
| username | String(50) | NULL | 사용자명 (입력된 경우) |
| ip_address | String(45) | NOT NULL | 요청 IP |
| success | Boolean | NOT NULL | 성공 여부 |
| attempted_at | DateTime | NOT NULL, DEFAULT now | 시도 시각 |

**용도**: 브루트포스 방지 (IP + 계정 복합 제한)

---

## 3. 인덱스 전략

| 테이블 | 인덱스 | 컬럼 | 용도 |
|--------|--------|------|------|
| Order | idx_order_store_session | store_id, session_id | 세션별 주문 조회 |
| Order | idx_order_store_date | store_id, created_at | 일별 주문 조회 |
| Order | idx_order_status | store_id, status, is_deleted | 상태별 주문 필터 |
| OrderItem | idx_orderitem_order | order_id | 주문별 항목 조회 |
| OrderHistory | idx_history_store_table | store_id, table_id, archived_at | 테이블별 과거 내역 |
| Menu | idx_menu_store_category | store_id, category_id, sort_order | 카테고리별 메뉴 조회 |
| TableSession | idx_session_table_active | table_id, is_active | 활성 세션 조회 |
| LoginAttempt | idx_login_ip_time | ip_address, attempted_at | IP별 시도 횟수 조회 |
| LoginAttempt | idx_login_account_time | store_id, username, attempted_at | 계정별 시도 횟수 조회 |

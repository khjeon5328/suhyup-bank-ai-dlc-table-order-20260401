# Unit 1: database - 도메인 엔티티 정의

> 담당자: 지현

---

## 엔티티 관계 다이어그램 (ERD)

```
+-------------+       +-------------+       +-------------+
|   Store     |1----N |    User     |       |  Category   |
|-------------|       |-------------|       |-------------|
| id (PK)     |       | id (PK)     |       | id (PK)     |
| name        |       | store_id(FK)|       | store_id(FK)|
| code (UQ)   |       | username    |       | name        |
| address     |       | password    |       | sort_order  |
| phone       |       | role        |       | created_at  |
| created_at  |       | created_at  |       +------+------+
| updated_at  |       | updated_at  |              |
+------+------+       +-------------+              |
       |                                           |
       |1                                         1|
       |                                           |
       |N                                          |N
+------+------+                             +------+------+
|   Table     |                             |    Menu     |
|-------------|                             |-------------|
| id (PK)     |                             | id (PK)     |
| store_id(FK)|                             | store_id(FK)|
| table_no    |                             | category_id |
| password    |                             | name        |
| status      |                             | price       |
| created_at  |                             | description |
| updated_at  |                             | image_url   |
+------+------+                             | sort_order  |
       |                                    | is_available|
       |1                                   | created_at  |
       |                                    | updated_at  |
       |N                                   +-------------+
+------+------+
|TableSession |
|-------------|       +-------------+       +-------------+
| id (PK)     |1----N |   Order     |1----N | OrderItem   |
| store_id(FK)|       |-------------|       |-------------|
| table_id(FK)|       | id (PK)     |       | id (PK)     |
| session_code|       | store_id(FK)|       | order_id(FK)|
| started_at  |       | table_id(FK)|       | menu_id(FK) |
| ended_at    |       | session_id  |       | menu_name   |
| is_active   |       | order_no    |       | quantity     |
| created_at  |       | total_amount|       | unit_price  |
+-------------+       | status      |       | subtotal    |
                      | is_archived |       | created_at  |
                      | created_at  |       +-------------+
                      | updated_at  |
                      +-------------+
```

---

## 엔티티 상세 정의

### Store (매장)

| 컬럼 | 타입 | 제약조건 | 설명 |
|------|------|---------|------|
| id | BIGINT | PK, AUTO_INCREMENT | 매장 고유 ID |
| name | VARCHAR(100) | NOT NULL | 매장명 |
| code | VARCHAR(50) | NOT NULL, UNIQUE | 매장 식별 코드 (로그인용) |
| address | VARCHAR(255) | NULLABLE | 매장 주소 |
| phone | VARCHAR(20) | NULLABLE | 매장 전화번호 |
| created_at | DATETIME | NOT NULL, DEFAULT NOW | 생성 시각 |
| updated_at | DATETIME | NOT NULL, DEFAULT NOW ON UPDATE | 수정 시각 |

**인덱스**: `idx_store_code` (code) UNIQUE

---

### User (관리자 사용자)

| 컬럼 | 타입 | 제약조건 | 설명 |
|------|------|---------|------|
| id | BIGINT | PK, AUTO_INCREMENT | 사용자 고유 ID |
| store_id | BIGINT | FK → Store.id, NOT NULL | 소속 매장 |
| username | VARCHAR(50) | NOT NULL | 사용자명 |
| password_hash | VARCHAR(255) | NOT NULL | bcrypt 해시 비밀번호 |
| role | ENUM('owner','manager') | NOT NULL | 역할 |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | 활성 상태 |
| login_attempts | INT | NOT NULL, DEFAULT 0 | 연속 로그인 실패 횟수 |
| locked_until | DATETIME | NULLABLE | 계정 잠금 해제 시각 |
| created_at | DATETIME | NOT NULL, DEFAULT NOW | 생성 시각 |
| updated_at | DATETIME | NOT NULL, DEFAULT NOW ON UPDATE | 수정 시각 |

**인덱스**: `idx_user_store_username` (store_id, username) UNIQUE

---

### RestaurantTable (테이블)

| 컬럼 | 타입 | 제약조건 | 설명 |
|------|------|---------|------|
| id | BIGINT | PK, AUTO_INCREMENT | 테이블 고유 ID |
| store_id | BIGINT | FK → Store.id, NOT NULL | 소속 매장 |
| table_no | INT | NOT NULL | 테이블 번호 |
| password_hash | VARCHAR(255) | NOT NULL | bcrypt 해시 비밀번호 |
| status | ENUM('available','occupied','inactive') | NOT NULL, DEFAULT 'available' | 테이블 상태 |
| created_at | DATETIME | NOT NULL, DEFAULT NOW | 생성 시각 |
| updated_at | DATETIME | NOT NULL, DEFAULT NOW ON UPDATE | 수정 시각 |

**인덱스**: `idx_table_store_no` (store_id, table_no) UNIQUE

---

### TableSession (테이블 세션)

| 컬럼 | 타입 | 제약조건 | 설명 |
|------|------|---------|------|
| id | BIGINT | PK, AUTO_INCREMENT | 세션 고유 ID |
| store_id | BIGINT | FK → Store.id, NOT NULL | 소속 매장 |
| table_id | BIGINT | FK → RestaurantTable.id, NOT NULL | 테이블 |
| session_code | VARCHAR(36) | NOT NULL, UNIQUE | 세션 고유 코드 (UUID) |
| started_at | DATETIME | NOT NULL, DEFAULT NOW | 세션 시작 시각 |
| ended_at | DATETIME | NULLABLE | 세션 종료 시각 (이용 완료) |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | 활성 상태 |
| created_at | DATETIME | NOT NULL, DEFAULT NOW | 생성 시각 |

**인덱스**: `idx_session_table_active` (table_id, is_active)

---

### Category (메뉴 카테고리)

| 컬럼 | 타입 | 제약조건 | 설명 |
|------|------|---------|------|
| id | BIGINT | PK, AUTO_INCREMENT | 카테고리 고유 ID |
| store_id | BIGINT | FK → Store.id, NOT NULL | 소속 매장 |
| name | VARCHAR(50) | NOT NULL | 카테고리명 |
| sort_order | INT | NOT NULL, DEFAULT 0 | 노출 순서 |
| created_at | DATETIME | NOT NULL, DEFAULT NOW | 생성 시각 |

**인덱스**: `idx_category_store_order` (store_id, sort_order)

---

### Menu (메뉴)

| 컬럼 | 타입 | 제약조건 | 설명 |
|------|------|---------|------|
| id | BIGINT | PK, AUTO_INCREMENT | 메뉴 고유 ID |
| store_id | BIGINT | FK → Store.id, NOT NULL | 소속 매장 |
| category_id | BIGINT | FK → Category.id, NOT NULL | 카테고리 |
| name | VARCHAR(100) | NOT NULL | 메뉴명 |
| price | INT | NOT NULL | 가격 (원) |
| description | TEXT | NULLABLE | 메뉴 설명 |
| image_url | VARCHAR(500) | NULLABLE | 이미지 URL |
| sort_order | INT | NOT NULL, DEFAULT 0 | 노출 순서 |
| is_available | BOOLEAN | NOT NULL, DEFAULT TRUE | 판매 가능 여부 |
| created_at | DATETIME | NOT NULL, DEFAULT NOW | 생성 시각 |
| updated_at | DATETIME | NOT NULL, DEFAULT NOW ON UPDATE | 수정 시각 |

**인덱스**: `idx_menu_store_category` (store_id, category_id, sort_order)

---

### Order (주문)

| 컬럼 | 타입 | 제약조건 | 설명 |
|------|------|---------|------|
| id | BIGINT | PK, AUTO_INCREMENT | 주문 고유 ID |
| store_id | BIGINT | FK → Store.id, NOT NULL | 소속 매장 |
| table_id | BIGINT | FK → RestaurantTable.id, NOT NULL | 테이블 |
| session_id | BIGINT | FK → TableSession.id, NOT NULL | 테이블 세션 |
| order_no | VARCHAR(20) | NOT NULL | 주문 번호 (매장 내 고유) |
| total_amount | INT | NOT NULL | 총 주문 금액 |
| status | ENUM('pending','preparing','completed') | NOT NULL, DEFAULT 'pending' | 주문 상태 |
| is_archived | BOOLEAN | NOT NULL, DEFAULT FALSE | 아카이브 여부 (이용 완료 시) |
| created_at | DATETIME | NOT NULL, DEFAULT NOW | 주문 시각 |
| updated_at | DATETIME | NOT NULL, DEFAULT NOW ON UPDATE | 수정 시각 |

**인덱스**:
- `idx_order_store_table_session` (store_id, table_id, session_id)
- `idx_order_store_status` (store_id, status)
- `idx_order_store_archived` (store_id, is_archived)

---

### OrderItem (주문 항목)

| 컬럼 | 타입 | 제약조건 | 설명 |
|------|------|---------|------|
| id | BIGINT | PK, AUTO_INCREMENT | 항목 고유 ID |
| order_id | BIGINT | FK → Order.id, NOT NULL | 주문 |
| menu_id | BIGINT | FK → Menu.id, NULLABLE | 메뉴 (삭제 시 NULL) |
| menu_name | VARCHAR(100) | NOT NULL | 주문 시점 메뉴명 (스냅샷) |
| quantity | INT | NOT NULL | 수량 |
| unit_price | INT | NOT NULL | 주문 시점 단가 (스냅샷) |
| subtotal | INT | NOT NULL | 소계 (quantity * unit_price) |
| created_at | DATETIME | NOT NULL, DEFAULT NOW | 생성 시각 |

**인덱스**: `idx_orderitem_order` (order_id)

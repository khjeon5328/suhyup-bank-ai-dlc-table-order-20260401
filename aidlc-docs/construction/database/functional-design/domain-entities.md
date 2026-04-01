# Domain Entities - Unit 1: database

---

## 엔티티 관계 다이어그램 (ERD)

```
+----------------+       +----------------+       +----------------+
|     Store      |       |     User       |       |   Category     |
+----------------+       +----------------+       +----------------+
| PK store_code  |<--+   | PK id (INT AI) |   +-->| PK id (INT AI) |
|    name        |   |   |    store_code  |---+   |    store_code  |---+
|    address     |   |   |    username    |       |    name        |   |
|    phone       |   |   |    password    |       |    sort_order  |   |
|    created_at  |   |   |    role        |       |    created_at  |   |
|    updated_at  |   |   |    deleted_at  |       |    updated_at  |   |
+----------------+   |   |    created_at  |       +----------------+   |
        |            |   |    updated_at  |                            |
        |            |   +----------------+                            |
        |            |                                                 |
        |            |   +----------------+       +----------------+   |
        |            |   |     Table      |       |      Menu      |   |
        |            |   +----------------+       +----------------+   |
        |            +---| FK store_code  |   +-->| PK id (INT AI) |   |
        |                | PK table_no    |   |   |    store_code  |---+
        |                |    password    |   |   | FK category_id |---+
        |                |    created_at  |   |   |    name        |
        |                |    updated_at  |   |   |    price       |
        |                +----------------+   |   |    description |
        |                       |             |   |    image_url   |
        |                       |             |   |    sort_order  |
        |                       v             |   |    deleted_at  |
        |            +------------------+     |   |    created_at  |
        |            |  TableSession    |     |   |    updated_at  |
        |            +------------------+     |   +----------------+
        |            | PK id (INT AI)   |     |
        +------------|    store_code    |     |
                     |    table_no      |     |
                     |    started_at    |     |
                     |    ended_at      |     |
                     |    created_at    |     |
                     +------------------+     |
                            |                 |
                            v                 |
                     +------------------+     |
                     |     Order        |     |
                     +------------------+     |
                     | PK id (INT AI)   |     |
                     |    store_code    |-----+
                     |    table_no      |
                     | FK session_id    |
                     |    order_number  |
                     |    total_amount  |
                     |    status        |
                     |    archived_at   |
                     |    created_at    |
                     |    updated_at    |
                     +------------------+
                            |
                            v
                     +------------------+
                     |   OrderItem      |
                     +------------------+
                     | PK id (INT AI)   |
                     | FK order_id      |
                     | FK menu_id       |
                     |    menu_name     |
                     |    quantity      |
                     |    unit_price    |
                     |    subtotal      |
                     |    created_at    |
                     +------------------+
```

---

## 엔티티 상세 정의

### 1. Store (매장)

| 필드 | 타입 | 제약조건 | 설명 |
|------|------|---------|------|
| store_code | VARCHAR(20) | PK | 매장 고유 코드 (예: "PIZZA01") |
| name | VARCHAR(100) | NOT NULL | 매장명 |
| address | VARCHAR(255) | NULLABLE | 매장 주소 |
| phone | VARCHAR(20) | NULLABLE | 매장 전화번호 |
| created_at | DATETIME | NOT NULL, DEFAULT NOW | 생성 시각 |
| updated_at | DATETIME | NOT NULL, DEFAULT NOW, ON UPDATE NOW | 수정 시각 |

**인덱스**: PK(store_code)

---

### 2. User (관리자 계정)

| 필드 | 타입 | 제약조건 | 설명 |
|------|------|---------|------|
| id | INT | PK, AUTO_INCREMENT | 내부 식별자 |
| store_code | VARCHAR(20) | FK → Store, NOT NULL | 소속 매장 |
| username | VARCHAR(50) | NOT NULL | 사용자명 |
| password_hash | VARCHAR(255) | NOT NULL | bcrypt 해싱된 비밀번호 |
| role | ENUM('owner','manager') | NOT NULL | 역할 |
| deleted_at | DATETIME | NULLABLE | 소프트 삭제 시각 |
| created_at | DATETIME | NOT NULL, DEFAULT NOW | 생성 시각 |
| updated_at | DATETIME | NOT NULL, DEFAULT NOW, ON UPDATE NOW | 수정 시각 |

**인덱스**: PK(id), UNIQUE(store_code, username) WHERE deleted_at IS NULL, FK(store_code)
**소프트 삭제**: 적용 (deleted_at)

---

### 3. RestaurantTable (테이블)

> 테이블명: `restaurant_table` (MySQL 예약어 `table` 회피)

| 필드 | 타입 | 제약조건 | 설명 |
|------|------|---------|------|
| store_code | VARCHAR(20) | PK(복합), FK → Store | 소속 매장 |
| table_no | INT | PK(복합) | 테이블 번호 |
| password_hash | VARCHAR(255) | NOT NULL | bcrypt 해싱된 PIN (4~6자리 숫자) |
| created_at | DATETIME | NOT NULL, DEFAULT NOW | 생성 시각 |
| updated_at | DATETIME | NOT NULL, DEFAULT NOW, ON UPDATE NOW | 수정 시각 |

**인덱스**: PK(store_code, table_no)
**복합 PK 이유**: 매장 내에서 테이블 번호는 고유하며, 매장 간에는 동일 번호 허용

---

### 4. TableSession (테이블 세션)

| 필드 | 타입 | 제약조건 | 설명 |
|------|------|---------|------|
| id | INT | PK, AUTO_INCREMENT | 세션 식별자 |
| store_code | VARCHAR(20) | FK → Store, NOT NULL | 매장 코드 |
| table_no | INT | NOT NULL | 테이블 번호 |
| started_at | DATETIME | NOT NULL, DEFAULT NOW | 세션 시작 시각 |
| ended_at | DATETIME | NULLABLE | 세션 종료 시각 (NULL=활성) |
| created_at | DATETIME | NOT NULL, DEFAULT NOW | 레코드 생성 시각 |

**인덱스**: PK(id), FK(store_code, table_no), IDX(store_code, table_no, ended_at)
**상태 판단**: `ended_at IS NULL` → 활성 세션, `ended_at IS NOT NULL` → 종료된 세션
**제약**: 동일 테이블에 활성 세션은 최대 1개

---

### 5. Category (메뉴 카테고리)

| 필드 | 타입 | 제약조건 | 설명 |
|------|------|---------|------|
| id | INT | PK, AUTO_INCREMENT | 카테고리 식별자 |
| store_code | VARCHAR(20) | FK → Store, NOT NULL | 소속 매장 |
| name | VARCHAR(50) | NOT NULL | 카테고리명 |
| sort_order | INT | NOT NULL, DEFAULT 0 | 노출 순서 |
| created_at | DATETIME | NOT NULL, DEFAULT NOW | 생성 시각 |
| updated_at | DATETIME | NOT NULL, DEFAULT NOW, ON UPDATE NOW | 수정 시각 |

**인덱스**: PK(id), UNIQUE(store_code, name), IDX(store_code, sort_order)

---

### 6. Menu (메뉴)

| 필드 | 타입 | 제약조건 | 설명 |
|------|------|---------|------|
| id | INT | PK, AUTO_INCREMENT | 메뉴 식별자 |
| store_code | VARCHAR(20) | FK → Store, NOT NULL | 소속 매장 |
| category_id | INT | FK → Category, NOT NULL | 카테고리 |
| name | VARCHAR(100) | NOT NULL | 메뉴명 |
| price | INT | NOT NULL, CHECK(price >= 0) | 가격 (원 단위) |
| description | TEXT | NULLABLE | 메뉴 설명 |
| image_url | VARCHAR(500) | NULLABLE | 메뉴 이미지 URL |
| sort_order | INT | NOT NULL, DEFAULT 0 | 노출 순서 |
| deleted_at | DATETIME | NULLABLE | 소프트 삭제 시각 |
| created_at | DATETIME | NOT NULL, DEFAULT NOW | 생성 시각 |
| updated_at | DATETIME | NOT NULL, DEFAULT NOW, ON UPDATE NOW | 수정 시각 |

**인덱스**: PK(id), FK(store_code), FK(category_id), IDX(store_code, category_id, sort_order)
**소프트 삭제**: 적용 (deleted_at) — 기존 주문이 참조할 수 있으므로

---

### 7. Order (주문)

| 필드 | 타입 | 제약조건 | 설명 |
|------|------|---------|------|
| id | INT | PK, AUTO_INCREMENT | 주문 식별자 (= 주문 번호) |
| store_code | VARCHAR(20) | FK → Store, NOT NULL | 매장 코드 |
| table_no | INT | NOT NULL | 테이블 번호 |
| session_id | INT | FK → TableSession, NOT NULL | 세션 ID |
| total_amount | INT | NOT NULL, CHECK(total_amount >= 0) | 총 주문 금액 (원) |
| status | ENUM('pending','preparing','completed') | NOT NULL, DEFAULT 'pending' | 주문 상태 |
| archived_at | DATETIME | NULLABLE | 아카이브 시각 (NULL=현재, NOT NULL=과거) |
| created_at | DATETIME | NOT NULL, DEFAULT NOW | 주문 시각 |
| updated_at | DATETIME | NOT NULL, DEFAULT NOW, ON UPDATE NOW | 수정 시각 |

**인덱스**: PK(id), FK(store_code), FK(session_id), IDX(store_code, table_no, archived_at), IDX(store_code, archived_at, created_at)
**주문 번호**: `id` (auto-increment)를 주문 번호로 직접 사용
**아카이브**: `archived_at IS NULL` → 현재 주문, `archived_at IS NOT NULL` → 과거 이력

---

### 8. OrderItem (주문 항목)

| 필드 | 타입 | 제약조건 | 설명 |
|------|------|---------|------|
| id | INT | PK, AUTO_INCREMENT | 항목 식별자 |
| order_id | INT | FK → Order, NOT NULL | 주문 ID |
| menu_id | INT | FK → Menu, NOT NULL | 메뉴 ID |
| menu_name | VARCHAR(100) | NOT NULL | 주문 시점 메뉴명 (스냅샷) |
| quantity | INT | NOT NULL, CHECK(quantity > 0) | 수량 |
| unit_price | INT | NOT NULL, CHECK(unit_price >= 0) | 주문 시점 단가 (스냅샷) |
| subtotal | INT | NOT NULL | 소계 (quantity * unit_price) |
| created_at | DATETIME | NOT NULL, DEFAULT NOW | 생성 시각 |

**인덱스**: PK(id), FK(order_id), FK(menu_id)
**스냅샷 필드**: `menu_name`, `unit_price`는 주문 시점의 값을 저장 (메뉴 수정/삭제 후에도 원본 유지)

---

## 엔티티 관계 요약

| 관계 | 유형 | 설명 |
|------|------|------|
| Store → User | 1:N | 매장당 여러 관리자 |
| Store → RestaurantTable | 1:N | 매장당 여러 테이블 |
| Store → Category | 1:N | 매장당 여러 카테고리 |
| Store → Menu | 1:N | 매장당 여러 메뉴 |
| Store → Order | 1:N | 매장당 여러 주문 |
| Category → Menu | 1:N | 카테고리당 여러 메뉴 |
| RestaurantTable → TableSession | 1:N | 테이블당 여러 세션 (시간순) |
| TableSession → Order | 1:N | 세션당 여러 주문 |
| Order → OrderItem | 1:N | 주문당 여러 항목 |
| Menu → OrderItem | 1:N | 메뉴당 여러 주문 항목 |

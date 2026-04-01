# Business Rules - Unit 1: database

---

## 1. 데이터 검증 규칙

### BR-01: Store 검증
- `store_code`: 1~20자, 영문 대문자+숫자만 허용 (정규식: `^[A-Z0-9]{1,20}$`)
- `name`: 1~100자, 필수

### BR-02: User 검증
- `username`: 1~50자, 매장 내 고유 (활성 계정 기준)
- `password`: 평문 최소 8자, bcrypt 해싱 후 저장
- `role`: 'owner' 또는 'manager'만 허용
- 매장당 최소 1명의 owner 필수 (마지막 owner 삭제 불가)

### BR-03: RestaurantTable 검증
- `table_no`: 양의 정수 (1 이상)
- `password`: 평문 4~6자리 숫자 PIN, bcrypt 해싱 후 저장
- 매장 내 table_no 고유

### BR-04: Category 검증
- `name`: 1~50자, 매장 내 고유
- `sort_order`: 0 이상 정수

### BR-05: Menu 검증
- `name`: 1~100자, 필수
- `price`: 0 이상 정수 (원 단위)
- `category_id`: 동일 매장의 유효한 카테고리 참조 필수
- `image_url`: 500자 이내, URL 형식 (선택)
- `sort_order`: 0 이상 정수

### BR-06: Order 검증
- 최소 1개 이상의 OrderItem 필수
- `total_amount`: OrderItem의 subtotal 합계와 일치해야 함
- 활성 세션(ended_at IS NULL)에서만 주문 생성 가능

### BR-07: OrderItem 검증
- `quantity`: 1 이상 정수
- `unit_price`: 0 이상 정수
- `subtotal`: quantity * unit_price와 일치해야 함
- `menu_name`, `unit_price`: 주문 생성 시점의 Menu 데이터에서 스냅샷

---

## 2. 참조 무결성 규칙

### RI-01: 매장 삭제 제한
- 하위 데이터(User, Table, Category, Menu, Order)가 존재하면 매장 삭제 불가
- CASCADE 삭제 미적용 (데이터 보호)

### RI-02: 카테고리 삭제 제한
- 해당 카테고리에 활성 메뉴(deleted_at IS NULL)가 존재하면 삭제 불가
- 소프트 삭제된 메뉴만 있으면 삭제 허용

### RI-03: 메뉴 소프트 삭제
- 메뉴 삭제 시 하드 삭제 대신 `deleted_at` 타임스탬프 기록
- 소프트 삭제된 메뉴는 고객 메뉴 조회에서 제외
- OrderItem이 참조하는 메뉴는 소프트 삭제 후에도 데이터 유지

### RI-04: 사용자 소프트 삭제
- 사용자 삭제 시 `deleted_at` 타임스탬프 기록
- 소프트 삭제된 사용자는 로그인 불가
- 동일 username 재사용 가능 (deleted_at IS NULL 조건의 unique 제약)

### RI-05: 주문-세션 연결
- 주문은 반드시 유효한 session_id를 참조
- 세션 종료 후에도 주문 데이터는 유지 (아카이브)

---

## 3. 상태 전이 규칙

### ST-01: 주문 상태 전이
```
pending → preparing → completed
```
- 순방향 전이만 허용 (역방향 불가)
- pending → preparing: 관리자가 주문 확인
- preparing → completed: 관리자가 준비 완료 처리
- 어떤 상태에서든 주문 삭제 가능 (점주만)

### ST-02: 테이블 세션 라이프사이클
```
[세션 없음] → ACTIVE (started_at 기록) → COMPLETED (ended_at 기록)
```
- 첫 주문 생성 시 활성 세션이 없으면 자동 생성 (started_at = NOW)
- 이용 완료 시 ended_at 기록
- 이용 완료 후 새 주문 시 새 세션 자동 생성
- 동일 테이블에 활성 세션은 최대 1개

### ST-03: 주문 아카이브 전이
```
현재 주문 (archived_at IS NULL) → 과거 이력 (archived_at = 이용완료시각)
```
- 테이블 이용 완료 시 해당 세션의 모든 주문에 archived_at 기록
- 아카이브된 주문은 고객 주문 내역에서 제외
- 아카이브된 주문은 관리자 과거 내역에서 조회 가능

---

## 4. 비즈니스 제약조건

### BC-01: 멀티 매장 데이터 격리
- 모든 데이터 조회/수정은 store_code 기준으로 필터링
- 매장 A의 관리자가 매장 B의 데이터에 접근 불가
- API 레벨에서 store_code 검증 필수

### BC-02: 역할 기반 데이터 접근
- owner: 모든 데이터 CRUD 가능
- manager: 주문 조회/상태변경, 테이블 세션 처리, 과거 내역 조회만 가능
- table: 해당 테이블의 메뉴 조회, 주문 생성/조회만 가능

### BC-03: 주문 금액 정합성
- OrderItem.subtotal = quantity * unit_price (애플리케이션 레벨 계산)
- Order.total_amount = SUM(OrderItem.subtotal) (애플리케이션 레벨 계산)
- 금액 불일치 시 주문 생성 거부

### BC-04: 세션 기반 주문 필터링
- 고객 주문 내역: 현재 활성 세션(ended_at IS NULL)의 주문 중 archived_at IS NULL인 것만 표시
- 관리자 현재 주문: archived_at IS NULL인 주문
- 관리자 과거 내역: archived_at IS NOT NULL인 주문, 날짜 필터 가능

### BC-05: 시드 데이터 규칙
- 시드 데이터는 개발/테스트 환경에서만 실행
- 기존 데이터가 있으면 시드 실행 건너뜀 (멱등성)
- 시드 비밀번호는 bcrypt 해싱 적용

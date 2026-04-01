# Backend - 비즈니스 로직 모델

---

## 1. BE-AUTH: 인증/인가 플로우

### 1.1 관리자 로그인 플로우

```
[요청] POST /api/v1/auth/login/admin
  |
  v
[입력 검증] store_code, username, password 필수
  |
  v
[브루트포스 검사]
  |-- IP 기반: 최근 15분 내 동일 IP에서 20회 이상 실패 → 429 차단
  |-- 계정 기반: 최근 15분 내 동일 store+username 5회 이상 실패 → 423 잠금
  |
  v
[매장 조회] store_code로 Store 조회 → 없으면 401
  |
  v
[사용자 조회] store_id + username으로 User 조회 → 없으면 401
  |
  v
[비밀번호 검증] bcrypt.verify(password, password_hash) → 실패 시 401
  |
  v
[LoginAttempt 기록] success=true
  |
  v
[JWT 발급] payload: {user_id, store_id, role, exp(16h)}
  |
  v
[응답] {access_token, token_type, expires_in, user: {id, username, role, store_id}}
```

### 1.2 테이블 로그인 플로우

```
[요청] POST /api/v1/auth/login/table
  |
  v
[입력 검증] store_code, table_no, password 필수
  |
  v
[매장 조회] store_code로 Store 조회 → 없으면 401
  |
  v
[테이블 조회] store_id + table_no로 Table 조회 → 없으면 401
  |
  v
[비밀번호 검증] bcrypt.verify → 실패 시 401
  |
  v
[활성 세션 확인] 해당 테이블의 is_active=true 세션 조회
  |
  v
[JWT 발급] payload: {table_id, store_id, session_id, role:"table", exp: 없음(무제한)}
  |
  v
[응답] {access_token, token_type, table: {id, table_no, store_id, session_id}}
```

### 1.3 토큰 검증 미들웨어

```
[모든 보호된 요청]
  |
  v
[Authorization 헤더 추출] Bearer {token}
  |
  v
[JWT 디코딩] 서명 검증 + 만료 확인
  |-- 실패 → 401 Unauthorized
  |
  v
[역할 확인] 요청 엔드포인트의 required_role과 토큰 role 비교
  |-- 권한 부족 → 403 Forbidden
  |
  v
[매장 소유권 확인] URL의 store_id와 토큰의 store_id 일치 확인
  |-- 불일치 → 403 Forbidden
  |
  v
[요청 처리 계속]
```

---

## 2. BE-TABLE: 테이블 세션 라이프사이클

### 2.1 테이블 초기 설정

```
[요청] POST /api/v1/stores/{store_id}/tables
  |-- 권한: owner만
  |
  v
[입력 검증] table_no(정수, 1이상), password(문자열, 4자 이상)
  |
  v
[중복 확인] store_id + table_no 중복 → 409 Conflict
  |
  v
[테이블 생성] password bcrypt 해싱 후 저장
  |
  v
[세션 자동 생성] TableSession(is_active=true) 생성
  |
  v
[응답] {table: {...}, session: {...}}
```

### 2.2 이용 완료 처리

```
[요청] POST /api/v1/stores/{store_id}/tables/{table_id}/session/end
  |-- 권한: owner, manager
  |
  v
[활성 세션 조회] table_id의 is_active=true 세션
  |-- 없으면 → 404 "활성 세션 없음"
  |
  v
[미완료 주문 확인] 해당 세션의 is_deleted=false AND status != completed 주문 조회
  |-- 미완료 주문 존재 시:
  |   [경고 응답] 422 {warning: "미완료 주문 N건 존재", pending_orders: [...]}
  |   → 클라이언트에서 force=true 파라미터로 재요청 가능
  |
  v
[주문 아카이브] 해당 세션의 모든 주문(is_deleted=false) → OrderHistory로 복사
  |
  v
[세션 종료] is_active=false, ended_at=now
  |
  v
[새 세션 생성] TableSession(is_active=true) 생성
  |
  v
[SSE 이벤트 발행] {type: "session_ended", table_id, session_id}
  |
  v
[응답] {old_session: {...}, new_session: {...}, archived_orders: N}
```

### 2.3 테이블 세션 상태 다이어그램

```
+------------------+
| 테이블 초기 설정  |
+--------+---------+
         |
         v
+--------+---------+
| 세션 활성 (대기)  |<---------+
| is_active=true   |          |
+--------+---------+          |
         |                    |
         | (주문 생성)         |
         v                    |
+--------+---------+          |
| 세션 활성 (주문중)|          |
| 주문 N건 존재    |          |
+--------+---------+          |
         |                    |
         | (이용 완료)         |
         v                    |
+--------+---------+          |
| 세션 종료         |          |
| is_active=false  |          |
| 주문 아카이브     +----------+
| 새 세션 자동 생성  | (새 세션)
+------------------+
```

---

## 3. BE-MENU: 메뉴 CRUD 로직

### 3.1 메뉴 등록

```
[요청] POST /api/v1/stores/{store_id}/menus
  |-- 권한: owner만
  |
  v
[입력 검증]
  |-- name: 필수, 1~100자
  |-- price: 필수, 0 이상 정수
  |-- category_id: 필수, 해당 매장의 유효한 카테고리
  |-- description: 선택, 최대 1000자
  |-- image_url: 선택, URL 형식 검증
  |
  v
[카테고리 존재 확인] store_id + category_id → 없으면 404
  |
  v
[sort_order 자동 설정] 해당 카테고리 내 최대 sort_order + 1
  |
  v
[메뉴 생성] DB 저장
  |
  v
[응답] 201 {menu: {...}}
```

### 3.2 메뉴 수정

```
[요청] PUT /api/v1/stores/{store_id}/menus/{menu_id}
  |-- 권한: owner만
  |
  v
[메뉴 조회] store_id + menu_id → 없으면 404
  |
  v
[입력 검증] 변경 필드만 검증 (부분 업데이트)
  |
  v
[카테고리 변경 시] 새 카테고리 존재 확인
  |
  v
[메뉴 업데이트] DB 저장
  |
  v
[응답] {menu: {...}}
```

### 3.3 메뉴 삭제

```
[요청] DELETE /api/v1/stores/{store_id}/menus/{menu_id}
  |-- 권한: owner만
  |
  v
[메뉴 조회] store_id + menu_id → 없으면 404
  |
  v
[논리적 삭제] is_active=false
  |
  v
[응답] 204 No Content
```

### 3.4 카테고리 CRUD

```
[등록] POST /api/v1/stores/{store_id}/menus/categories
  |-- 권한: owner만
  |-- 입력: name(필수, 1~50자)
  |-- 중복 확인: store_id + name → 409
  |-- sort_order 자동 설정

[수정] PUT /api/v1/stores/{store_id}/menus/categories/{category_id}
  |-- 권한: owner만
  |-- name 변경 시 중복 확인

[삭제] DELETE /api/v1/stores/{store_id}/menus/categories/{category_id}
  |-- 권한: owner만
  |-- 해당 카테고리에 활성 메뉴 존재 시 → 409 "메뉴가 존재하는 카테고리는 삭제 불가"
```

---

## 4. BE-ORDER: 주문 생성/상태 관리/아카이브

### 4.1 주문 생성

```
[요청] POST /api/v1/stores/{store_id}/orders
  |-- 권한: table
  |
  v
[입력 검증]
  |-- items: 필수, 1개 이상
  |-- 각 item: menu_id(필수), quantity(필수, 1이상)
  |
  v
[세션 확인] 토큰의 session_id로 활성 세션 확인 → 없으면 403
  |
  v
[메뉴 유효성 확인] 각 menu_id가 해당 매장의 활성 메뉴인지 확인
  |-- 비활성/미존재 메뉴 → 400 "유효하지 않은 메뉴"
  |
  v
[주문 번호 생성] 매장별 오늘 날짜 기준 순번 (SELECT MAX + 1, 동시성 처리)
  |
  v
[주문 생성]
  |-- Order 레코드 생성 (status=pending)
  |-- OrderItem 레코드 생성 (menu_name, unit_price 스냅샷 저장)
  |-- total_amount 계산 (SUM of subtotals)
  |
  v
[SSE 이벤트 발행] {type: "order_created", order: {...}}
  |
  v
[응답] 201 {order: {id, order_no, items, total_amount, status, created_at}}
```

### 4.2 주문 상태 변경

```
[요청] PATCH /api/v1/stores/{store_id}/orders/{order_id}/status
  |-- 권한: owner, manager
  |
  v
[주문 조회] store_id + order_id, is_deleted=false → 없으면 404
  |
  v
[상태 전이 검증] 순방향만 허용
  |-- pending → preparing: OK
  |-- preparing → completed: OK
  |-- 그 외: 400 "허용되지 않는 상태 전이"
  |
  v
[상태 업데이트] DB 저장
  |
  v
[SSE 이벤트 발행] {type: "order_status_changed", order_id, old_status, new_status}
  |
  v
[응답] {order: {...}}
```

### 4.3 주문 삭제 (논리적)

```
[요청] DELETE /api/v1/stores/{store_id}/orders/{order_id}
  |-- 권한: owner만
  |
  v
[주문 조회] store_id + order_id, is_deleted=false → 없으면 404
  |
  v
[논리적 삭제] is_deleted=true, deleted_at=now
  |
  v
[SSE 이벤트 발행] {type: "order_deleted", order_id, table_id}
  |
  v
[응답] 204 No Content
```

### 4.4 주문 번호 생성 로직

```
매장별 일일 순번 생성:
1. 오늘 날짜의 해당 매장 최대 order_no 조회
   SELECT MAX(CAST(order_no AS UNSIGNED))
   FROM orders
   WHERE store_id = ? AND DATE(created_at) = CURDATE()
2. 결과 + 1 (없으면 1부터 시작)
3. 3자리 zero-padding (예: "001", "002", ...)
4. 동시성 처리: DB 트랜잭션 + SELECT FOR UPDATE 또는 재시도 로직
```

### 4.5 주문 아카이브 로직

```
archive_session_orders(store_id, table_id, session_id):
  |
  v
[주문 조회] session_id의 is_deleted=false 주문 전체
  |
  v
[각 주문에 대해]
  |-- OrderItem 조회
  |-- OrderHistory 레코드 생성:
  |   - order_data: JSON {items: [{menu_name, quantity, unit_price, subtotal}]}
  |   - 원본 주문 정보 복사
  |
  v
[원본 주문 논리적 삭제] is_deleted=true (아카이브 완료 표시)
  |
  v
[반환] 아카이브된 주문 수
```

---

## 5. BE-SSE: 이벤트 브로드캐스트 로직

### 5.1 연결 관리

```
[관리자 SSE 연결] GET /api/v1/stores/{store_id}/events/admin
  |-- 권한: owner, manager
  |-- 매장별 관리자 연결 풀에 추가
  |-- 이벤트: order_created, order_status_changed, order_deleted, session_ended

[테이블 SSE 연결] GET /api/v1/stores/{store_id}/events/table/{table_id}
  |-- 권한: table (해당 테이블만)
  |-- 테이블별 연결 풀에 추가
  |-- 이벤트: order_status_changed (해당 테이블 주문만)
```

### 5.2 이벤트 구조

```json
{
  "event": "order_created",
  "data": {
    "type": "order_created",
    "store_id": 1,
    "table_id": 3,
    "order": {
      "id": 42,
      "order_no": "005",
      "table_no": 3,
      "items": [...],
      "total_amount": 25000,
      "status": "pending",
      "created_at": "2026-04-01T12:30:00Z"
    }
  }
}
```

### 5.3 브로드캐스트 대상

| 이벤트 | 관리자 (매장 전체) | 테이블 (해당 테이블만) |
|--------|:-----------------:|:--------------------:|
| order_created | O | X |
| order_status_changed | O | O |
| order_deleted | O | X |
| session_ended | O | O |

### 5.4 연결 풀 구조

```
SSEManager:
  connections: Dict[int, Dict[str, List[EventStream]]]
  |
  +-- store_id:
       +-- "admin": [connection1, connection2, ...]
       +-- "table_{table_id}": [connection1, ...]
```

---

## 6. BE-USER: 계정 관리 로직

### 6.1 계정 생성

```
[요청] POST /api/v1/stores/{store_id}/users
  |-- 권한: owner만
  |
  v
[입력 검증]
  |-- username: 필수, 3~50자, 영문+숫자+밑줄
  |-- password: 필수, 8자 이상
  |-- role: 필수, owner 또는 manager
  |
  v
[중복 확인] store_id + username → 409
  |
  v
[비밀번호 해싱] bcrypt
  |
  v
[계정 생성] DB 저장
  |
  v
[응답] 201 {user: {id, username, role, created_at}} (password 제외)
```

### 6.2 계정 수정/삭제

```
[수정] PUT /api/v1/stores/{store_id}/users/{user_id}
  |-- 권한: owner만
  |-- 변경 가능: username, password, role
  |-- 자기 자신의 role 변경 불가 (owner → manager 방지)

[삭제] DELETE /api/v1/stores/{store_id}/users/{user_id}
  |-- 권한: owner만
  |-- 자기 자신 삭제 불가
  |-- 매장의 마지막 owner 삭제 불가
```

---

## 7. BE-IMAGE: 이미지 업로드 로직

### 7.1 Presigned URL 생성

```
[요청] POST /api/v1/stores/{store_id}/images/presigned-url
  |-- 권한: owner만
  |
  v
[입력 검증]
  |-- filename: 필수
  |-- content_type: 필수, image/jpeg|image/png|image/webp만 허용
  |
  v
[파일명 생성] {store_id}/{uuid}.{extension}
  |
  v
[S3 Presigned URL 생성] boto3, PUT 메서드, 만료 300초
  |
  v
[응답] {upload_url, image_url, expires_in: 300}
```

---

## 8. BE-STORE: 매장 관리 로직

```
[매장 조회] GET /api/v1/stores/{store_id}
  |-- 권한: 인증된 사용자 (해당 매장 소속)
  |-- 응답: {store: {id, name, code, address, phone}}

[매장 목록] (시드 데이터 기반, 관리 API 없음)
```

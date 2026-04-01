# Backend - 비즈니스 규칙 정의

---

## 1. 인증/인가 규칙

### BR-AUTH-01: JWT 토큰 정책
| 항목 | 관리자 토큰 | 테이블 토큰 |
|------|-----------|-----------|
| 유효 기간 | 16시간 | 무제한 |
| 갱신 방식 | 재로그인 | 불필요 |
| Payload | user_id, store_id, role | table_id, store_id, session_id, role:"table" |
| 알고리즘 | HS256 | HS256 |

### BR-AUTH-02: 역할 기반 접근 제어 (RBAC)

| API 엔드포인트 | owner | manager | table |
|---------------|:-----:|:-------:|:-----:|
| POST /auth/login/* | 공개 | 공개 | 공개 |
| GET /stores/{id} | O | O | O |
| GET /tables | O | O | X |
| POST /tables | O | X | X |
| POST /tables/{id}/session/end | O | O | X |
| GET /tables/{id}/history | O | O | X |
| GET /menus | O | O | O |
| POST /menus | O | X | X |
| PUT /menus/{id} | O | X | X |
| DELETE /menus/{id} | O | X | X |
| PUT /menus/order | O | X | X |
| GET/POST /menus/categories | O | X | X |
| PUT/DELETE /menus/categories/{id} | O | X | X |
| GET /orders | O | O | O* |
| POST /orders | X | X | O |
| GET /orders/{id} | O | O | O* |
| PATCH /orders/{id}/status | O | O | X |
| DELETE /orders/{id} | O | X | X |
| GET/POST /users | O | X | X |
| PUT/DELETE /users/{id} | O | X | X |
| POST /images/presigned-url | O | X | X |
| GET /events/admin | O | O | X |
| GET /events/table/{id} | X | X | O* |

*O*: 자신의 테이블/세션 데이터만 접근 가능

### BR-AUTH-03: 브루트포스 방지 규칙
| 규칙 | 임계값 | 차단 기간 | 대상 |
|------|--------|----------|------|
| IP Rate Limiting | 15분 내 20회 실패 | 15분 | 관리자 로그인 |
| 계정 잠금 | 15분 내 5회 실패 | 15분 | 관리자 로그인 |
| 테이블 로그인 | Rate Limiting 없음 | - | 태블릿 자동 로그인 |

### BR-AUTH-04: 매장 소유권 검증
- 모든 매장 리소스 접근 시 토큰의 store_id와 URL의 store_id 일치 확인
- 불일치 시 403 Forbidden 반환
- 테이블 토큰은 자신의 table_id 리소스만 접근 가능

---

## 2. 주문 규칙

### BR-ORDER-01: 주문 상태 전이
```
[pending] ---> [preparing] ---> [completed]
  (대기중)      (준비중)         (완료)
```
- 순방향만 허용: pending → preparing → completed
- 역방향 전이 불가 (preparing → pending 불가)
- 삭제된 주문(is_deleted=true)의 상태 변경 불가

### BR-ORDER-02: 주문 생성 규칙
- 활성 세션이 있는 테이블만 주문 가능
- 주문 항목 최소 1개 이상 필수
- 각 항목의 수량은 1 이상
- 메뉴는 해당 매장의 활성(is_active=true) 메뉴만 가능
- 주문 시점의 메뉴명과 단가를 스냅샷으로 저장 (이후 메뉴 변경에 영향 없음)
- total_amount = SUM(quantity * unit_price)

### BR-ORDER-03: 주문 번호 규칙
- 형식: 매장별 일일 순번 (3자리 zero-padding)
- 예시: "001", "002", ..., "999"
- 매일 자정 기준 리셋 (다음 날 "001"부터 시작)
- 매장별 독립 (매장 A의 "001"과 매장 B의 "001"은 별개)
- 동시성 처리: DB 트랜잭션으로 순번 충돌 방지

### BR-ORDER-04: 주문 삭제 규칙
- 점주(owner)만 삭제 가능
- 논리적 삭제 (is_deleted=true, deleted_at 기록)
- 삭제된 주문은 목록 조회에서 제외
- 삭제된 주문은 테이블 총 주문액 계산에서 제외
- 삭제 시 SSE 이벤트 발행

### BR-ORDER-05: 주문 조회 규칙
- 테이블(고객): 현재 활성 세션의 is_deleted=false 주문만 조회
- 관리자: 해당 매장의 활성 세션 주문 전체 조회 (is_deleted=false)
- 정렬: 주문 시각 기준 (최신순 또는 오래된순)

### BR-ORDER-06: 동시 주문 허용
- 같은 테이블에서 동시에 여러 주문 생성 허용
- 각 주문은 독립적인 주문 번호 부여
- 동시성 충돌은 DB 트랜잭션으로 처리

---

## 3. 테이블 세션 규칙

### BR-SESSION-01: 세션 라이프사이클
- 테이블 초기 설정(setup) 시 첫 세션 자동 생성
- 테이블당 활성 세션(is_active=true)은 최대 1개
- 이용 완료 시 현재 세션 종료 + 새 세션 자동 생성

### BR-SESSION-02: 이용 완료 처리 규칙
- 점주(owner) 또는 매니저(manager)가 실행 가능
- 미완료 주문(pending/preparing) 존재 시:
  - 첫 요청: 경고 응답 (422) + 미완료 주문 목록 반환
  - force=true 재요청: 강제 이용 완료 진행
- 처리 순서:
  1. 현재 세션의 is_deleted=false 주문 → OrderHistory로 아카이브
  2. 원본 주문 is_deleted=true 처리
  3. 현재 세션 is_active=false, ended_at 기록
  4. 새 세션 생성 (is_active=true)
  5. SSE 이벤트 발행

### BR-SESSION-03: 세션 기반 데이터 격리
- 고객은 현재 활성 세션의 주문만 조회 가능
- 이전 세션의 주문은 OrderHistory에서만 조회 (관리자)
- 세션 종료 후 해당 세션의 주문은 고객에게 표시되지 않음

---

## 4. 메뉴 규칙

### BR-MENU-01: 메뉴 데이터 검증
| 필드 | 검증 규칙 |
|------|----------|
| name | 필수, 1~100자 |
| price | 필수, 0 이상 정수 |
| category_id | 필수, 해당 매장의 활성 카테고리 |
| description | 선택, 최대 1000자 |
| image_url | 선택, URL 형식 |
| sort_order | 선택, 0 이상 정수 |

### BR-MENU-02: 메뉴 삭제 규칙
- 논리적 삭제 (is_active=false)
- 삭제된 메뉴는 고객 메뉴 조회에서 제외
- 기존 주문의 OrderItem에는 영향 없음 (스냅샷 저장)

### BR-MENU-03: 카테고리 규칙
- 시드 데이터로 기본 카테고리 제공
- 점주가 카테고리 추가/수정/삭제 가능
- 활성 메뉴가 있는 카테고리는 삭제 불가
- 매장 내 카테고리명 중복 불가

### BR-MENU-04: 노출 순서 규칙
- sort_order 값 기준 오름차순 정렬
- 동일 sort_order 시 생성 시각 기준
- 순서 변경 API로 일괄 업데이트 가능

---

## 5. 사용자 관리 규칙

### BR-USER-01: 계정 생성 규칙
| 필드 | 검증 규칙 |
|------|----------|
| username | 필수, 3~50자, 영문+숫자+밑줄만 |
| password | 필수, 8자 이상 |
| role | 필수, "owner" 또는 "manager" |

### BR-USER-02: 계정 보호 규칙
- 자기 자신의 역할(role) 변경 불가
- 자기 자신 삭제 불가
- 매장의 마지막 owner 계정 삭제 불가
- 비밀번호는 bcrypt로 해싱 저장
- 비밀번호는 API 응답에 절대 포함하지 않음

---

## 6. 이미지 업로드 규칙

### BR-IMAGE-01: 업로드 제약
| 항목 | 제약 |
|------|------|
| 허용 형식 | image/jpeg, image/png, image/webp |
| Presigned URL 만료 | 300초 (5분) |
| 파일명 | {store_id}/{uuid}.{extension} |
| 업로드 방식 | 클라이언트 → S3 직접 업로드 (Presigned URL) |

---

## 7. 에러 응답 규칙

### BR-ERROR-01: 표준 에러 응답 형식
```json
{
  "error_code": "ORDER_NOT_FOUND",
  "message": "주문을 찾을 수 없습니다.",
  "details": {
    "order_id": 42
  }
}
```

### BR-ERROR-02: HTTP 상태 코드 매핑
| 상태 코드 | 용도 |
|-----------|------|
| 400 | 입력값 검증 실패, 잘못된 요청 |
| 401 | 인증 실패 (토큰 없음/만료/잘못됨) |
| 403 | 권한 부족 (역할/매장 소유권) |
| 404 | 리소스 미존재 |
| 409 | 중복 충돌 (username, table_no, category name) |
| 422 | 비즈니스 규칙 위반 (미완료 주문 경고 등) |
| 423 | 계정 잠금 (브루트포스) |
| 429 | Rate Limit 초과 |
| 500 | 서버 내부 오류 (상세 정보 노출 금지) |

### BR-ERROR-03: 에러 코드 체계
| 접두사 | 모듈 | 예시 |
|--------|------|------|
| AUTH_ | 인증/인가 | AUTH_INVALID_CREDENTIALS, AUTH_TOKEN_EXPIRED |
| ORDER_ | 주문 | ORDER_NOT_FOUND, ORDER_INVALID_STATUS_TRANSITION |
| TABLE_ | 테이블 | TABLE_DUPLICATE, TABLE_NO_ACTIVE_SESSION |
| MENU_ | 메뉴 | MENU_NOT_FOUND, MENU_INVALID_PRICE |
| USER_ | 사용자 | USER_DUPLICATE, USER_CANNOT_DELETE_SELF |
| SESSION_ | 세션 | SESSION_PENDING_ORDERS, SESSION_NOT_FOUND |
| IMAGE_ | 이미지 | IMAGE_INVALID_TYPE |
| GENERAL_ | 공통 | GENERAL_VALIDATION_ERROR, GENERAL_INTERNAL_ERROR |

---

## 8. 데이터 무결성 규칙

### BR-DATA-01: 소프트 삭제 정책
| 엔티티 | 삭제 방식 | 필드 |
|--------|----------|------|
| Order | Soft Delete | is_deleted, deleted_at |
| Menu | Soft Delete | is_active=false |
| Category | Soft Delete | is_active=false |
| User | Soft Delete | is_active=false |
| Table | Soft Delete | is_active=false |

### BR-DATA-02: 스냅샷 정책
- OrderItem에 주문 시점의 menu_name, unit_price 저장
- 메뉴 가격/이름 변경이 기존 주문에 영향 없음
- OrderHistory에 주문 상세를 JSON으로 보존

### BR-DATA-03: 매장 데이터 격리
- 모든 쿼리에 store_id 조건 필수
- 매장 간 데이터 접근 불가
- API 레벨에서 store_id 검증 (토큰 vs URL)

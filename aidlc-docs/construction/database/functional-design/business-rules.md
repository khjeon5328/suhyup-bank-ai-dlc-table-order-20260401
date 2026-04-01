# Unit 1: database - 비즈니스 규칙

> 담당자: 지현

---

## BR-01: 매장 코드 고유성
- 매장 코드(code)는 시스템 전체에서 고유해야 한다
- 로그인 시 매장 식별에 사용

## BR-02: 사용자명 매장 내 고유성
- 동일 매장 내에서 사용자명(username)은 고유해야 한다
- 다른 매장에서는 동일 사용자명 허용

## BR-03: 테이블 번호 매장 내 고유성
- 동일 매장 내에서 테이블 번호(table_no)는 고유해야 한다

## BR-04: 비밀번호 해싱
- User.password_hash와 RestaurantTable.password_hash는 반드시 bcrypt로 해싱하여 저장
- 평문 비밀번호는 절대 저장하지 않음

## BR-05: 테이블 세션 라이프사이클
- 테이블당 활성 세션(is_active=TRUE)은 최대 1개
- 첫 주문 시 활성 세션이 없으면 새 세션 자동 생성
- 이용 완료 시: is_active=FALSE, ended_at 기록
- 이용 완료 후 새 주문 시 새 세션 생성

## BR-06: 주문 번호 생성
- 매장 내에서 고유한 주문 번호 생성
- 형식: `ORD-{YYYYMMDD}-{순번}` (예: ORD-20260401-001)
- 일자별 순번 리셋

## BR-07: 주문 상태 전이
- 허용 전이: pending → preparing → completed
- 역방향 전이 불가
- 삭제된 주문은 상태 변경 불가

## BR-08: 주문 금액 계산
- OrderItem.subtotal = quantity * unit_price
- Order.total_amount = SUM(OrderItem.subtotal)
- 가격은 주문 시점의 메뉴 가격을 스냅샷으로 저장 (menu_name, unit_price)

## BR-09: 주문 아카이브 (이용 완료)
- 이용 완료 시 해당 세션의 모든 주문에 is_archived=TRUE 설정
- 아카이브된 주문은 현재 주문 목록에서 제외
- 아카이브된 주문은 과거 내역에서 조회 가능

## BR-10: 메뉴 가격 제약
- price는 0 이상의 정수 (원 단위)
- 음수 가격 불허

## BR-11: 메뉴 삭제 시 주문 보존
- 메뉴 삭제 시 기존 OrderItem의 menu_id는 NULL로 설정 (SET NULL)
- menu_name, unit_price 스냅샷으로 주문 이력 보존

## BR-12: 로그인 시도 제한
- 연속 5회 로그인 실패 시 계정 잠금
- 잠금 시간: 15분
- 잠금 해제 후 login_attempts 리셋

## BR-13: 카테고리/메뉴 정렬
- sort_order 기준 오름차순 정렬
- 동일 sort_order 시 created_at 오름차순

## BR-14: 데이터 격리
- 모든 쿼리는 store_id 기반으로 매장 데이터 격리
- 다른 매장의 데이터에 접근 불가

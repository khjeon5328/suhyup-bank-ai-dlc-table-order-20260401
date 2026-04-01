# Functional Design 질문 - Unit 1: database

database 유닛의 상세 설계를 위해 아래 질문에 답변해 주세요.
각 질문의 `[Answer]:` 태그 뒤에 선택지 알파벳을 입력해 주세요.

---

## Question 1
테이블 세션(TableSession)의 상태 관리 방식을 어떻게 설계할까요?

A) 단순 플래그 방식 — `is_active` boolean 필드로 활성/비활성 구분
B) 상태 필드 방식 — `status` enum 필드 (ACTIVE, COMPLETED, CANCELLED 등)
C) 시간 기반 방식 — `started_at`, `ended_at` 필드로 NULL 여부로 상태 판단
D) Other (please describe after [Answer]: tag below)

[Answer]: C

---

## Question 2
주문(Order)이 이용 완료 처리 시 과거 이력으로 이동하는 방식을 어떻게 할까요?

A) 별도 테이블 방식 — OrderHistory 테이블로 데이터를 복사 후 원본 삭제
B) 소프트 삭제 방식 — Order 테이블에 `archived_at` 필드 추가, 아카이브 시 타임스탬프 기록 (원본 유지)
C) 파티션 방식 — 동일 테이블에서 `session_id`와 세션 상태로 현재/과거 구분
D) Other (please describe after [Answer]: tag below)

[Answer]: B

---

## Question 3
메뉴 카테고리(Category) 관리 방식을 어떻게 설계할까요?

A) 별도 테이블 — Category 테이블을 만들고 Menu에서 FK로 참조
B) Enum 방식 — Menu 테이블에 category 문자열 필드로 직접 저장
C) 계층형 카테고리 — Category 테이블에 parent_id를 두어 하위 카테고리 지원
D) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 4
매장(Store) 식별자의 형태를 어떻게 할까요?

A) 자동 증가 정수 ID — 내부 PK로만 사용, 별도 store_code(문자열) 필드를 로그인 시 사용
B) UUID — 고유 식별자로 사용
C) 사용자 정의 코드 — 매장 코드(예: "STORE001")를 PK로 사용
D) Other (please describe after [Answer]: tag below)

[Answer]: C

---

## Question 5
주문 번호(Order Number) 생성 전략을 어떻게 할까요?

A) 매장별 일일 순번 — 매장+날짜 기준 순차 번호 (예: 001, 002, ...)
B) 글로벌 자동 증가 — DB auto-increment ID를 주문 번호로 사용
C) 타임스탬프 기반 — 날짜+시간+순번 조합 (예: 20260401-001)
D) Other (please describe after [Answer]: tag below)

[Answer]: B

---

## Question 6
시드 데이터의 범위를 어떻게 설정할까요?

A) 최소 — 매장 1개, 관리자 1명(점주), 테이블 3개, 카테고리 2개, 메뉴 5개
B) 중간 — 매장 2개, 관리자 3명(점주+매니저), 테이블 5~10개, 카테고리 4개, 메뉴 15개
C) 풍부 — 매장 3개, 관리자 5명, 테이블 10~20개, 카테고리 6개, 메뉴 30개+, 샘플 주문 포함
D) Other (please describe after [Answer]: tag below)

[Answer]: B

---

## Question 7
소프트 삭제(Soft Delete) 전략을 어떻게 적용할까요?

A) 전체 적용 — 모든 주요 엔티티에 `deleted_at` 필드 추가 (Menu, User, Table 등)
B) 선택적 적용 — 메뉴와 사용자 계정에만 소프트 삭제 적용, 나머지는 하드 삭제
C) 미적용 — 소프트 삭제 없이 하드 삭제만 사용
D) Other (please describe after [Answer]: tag below)

[Answer]: B

---

## Question 8
메뉴 이미지 URL 저장 방식을 어떻게 할까요?

A) 단일 필드 — Menu 테이블에 `image_url` 문자열 필드 1개 (메인 이미지만)
B) 다중 이미지 — 별도 MenuImage 테이블로 메뉴당 여러 이미지 지원
C) JSON 필드 — Menu 테이블에 `images` JSON 필드로 여러 URL 저장
D) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 9
감사 추적(Audit Trail) 필드를 어떻게 적용할까요?

A) 기본 타임스탬프 — 모든 테이블에 `created_at`, `updated_at` 필드만 추가
B) 확장 감사 — 타임스탬프 + `created_by`, `updated_by` 필드 추가
C) 전체 감사 로그 — 별도 AuditLog 테이블에 모든 변경 이력 기록
D) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 10
테이블 비밀번호의 용도와 복잡도를 어떻게 설정할까요?

A) 단순 PIN — 4~6자리 숫자 PIN (태블릿 초기 설정용, bcrypt 해싱)
B) 일반 비밀번호 — 영문+숫자 조합 8자 이상 (bcrypt 해싱)
C) 자동 생성 토큰 — 시스템이 자동 생성하는 랜덤 토큰 (관리자가 직접 입력하지 않음)
D) Other (please describe after [Answer]: tag below)

[Answer]: A


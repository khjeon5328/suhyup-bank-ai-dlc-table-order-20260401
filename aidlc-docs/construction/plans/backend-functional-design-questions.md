# Backend Functional Design 질문

backend 유닛의 상세 비즈니스 로직 설계를 위해 아래 질문에 답변해 주세요.
각 질문의 `[Answer]:` 태그 뒤에 선택지 알파벳을 입력해 주세요.

---

## Question 1: 주문 상태 전이 모델
주문 상태 변경 시 역방향 전이(예: 준비중 → 대기중)를 허용할까요?

A) 순방향만 허용 (대기중 → 준비중 → 완료, 되돌리기 불가)
B) 역방향도 허용 (준비중 → 대기중 되돌리기 가능)
C) 점주만 역방향 허용, 매니저는 순방향만
X) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 2: 테이블 세션 시작 시점
테이블 세션은 언제 시작되나요?

A) 테이블 초기 설정(setup) 시 자동으로 세션 생성
B) 해당 테이블에서 첫 주문이 생성될 때 자동으로 세션 시작
C) 관리자가 수동으로 "세션 시작" 버튼을 클릭할 때
X) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 3: 이용 완료 시 활성 주문 처리
테이블 이용 완료 처리 시, 아직 "완료" 상태가 아닌 주문(대기중/준비중)이 있으면 어떻게 처리할까요?

A) 모든 주문 상태와 관계없이 이용 완료 허용 (미완료 주문도 그대로 아카이브)
B) 미완료 주문이 있으면 이용 완료 차단 (모든 주문이 완료 상태여야 함)
C) 경고 메시지 표시 후 관리자가 강제 이용 완료 가능
X) Other (please describe after [Answer]: tag below)

[Answer]: C

---

## Question 4: 주문 삭제 시 데이터 처리
점주가 주문을 삭제할 때 데이터를 어떻게 처리할까요?

A) 물리적 삭제 (DB에서 완전 제거)
B) 논리적 삭제 (soft delete - 삭제 플래그 설정, 데이터 보존)
C) 삭제된 주문을 별도 삭제 이력 테이블로 이동
X) Other (please describe after [Answer]: tag below)

[Answer]: B

---

## Question 5: JWT 토큰 갱신 전략
관리자 JWT 토큰(16시간 유효)의 갱신 방식은 어떻게 할까요?

A) Access Token만 사용 (16시간 후 재로그인)
B) Access Token + Refresh Token 조합 (Access 만료 시 Refresh로 자동 갱신)
C) Sliding Session (활동 시마다 만료 시간 연장)
X) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 6: 테이블 토큰 유효 기간
테이블 태블릿 자동 로그인 토큰의 유효 기간은 어떻게 설정할까요?

A) 무제한 (수동 변경 시까지 영구 유효)
B) 매우 긴 기간 (예: 365일) 후 자동 갱신
C) 24시간마다 자동 갱신 (백그라운드)
X) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 7: 브루트포스 방지 전략
로그인 시도 제한의 구체적인 방식은 어떻게 할까요?

A) IP 기반 Rate Limiting (예: 분당 5회 제한)
B) 계정 기반 잠금 (예: 5회 실패 시 15분 잠금)
C) IP + 계정 복합 (IP Rate Limiting + 계정 잠금 병행)
X) Other (please describe after [Answer]: tag below)

[Answer]: C

---

## Question 8: SSE 연결 관리
SSE 연결이 끊어졌을 때의 재연결 전략은 어떻게 할까요?

A) 클라이언트 자동 재연결 (EventSource 기본 동작 활용)
B) 클라이언트 자동 재연결 + 서버에서 놓친 이벤트 재전송 (Last-Event-ID 기반)
C) 클라이언트 자동 재연결 + 재연결 시 전체 데이터 새로고침
X) Other (please describe after [Answer]: tag below)

[Answer]: C

---

## Question 9: 메뉴 카테고리 관리
메뉴 카테고리는 어떻게 관리할까요?

A) 고정 카테고리 (시드 데이터로 미리 정의, 관리자가 변경 불가)
B) 관리자가 카테고리를 자유롭게 CRUD 가능
C) 시드 데이터로 기본 카테고리 제공 + 관리자가 추가/수정 가능
X) Other (please describe after [Answer]: tag below)

[Answer]: C

---

## Question 10: 주문 번호 생성 방식
주문 번호는 어떤 형식으로 생성할까요?

A) 자동 증가 정수 (1, 2, 3, ...)
B) 매장별 일일 순번 (예: 001, 002 - 매일 리셋)
C) UUID 기반 고유 식별자
D) 날짜+순번 조합 (예: 20260401-001)
X) Other (please describe after [Answer]: tag below)

[Answer]: B

---

## Question 11: 에러 응답 형식
API 에러 응답의 표준 형식은 어떻게 할까요?

A) 간단한 형식 (HTTP 상태 코드 + message 필드만)
B) 상세 형식 (HTTP 상태 코드 + error_code + message + details)
C) RFC 7807 Problem Details 표준 형식
X) Other (please describe after [Answer]: tag below)

[Answer]: B

---

## Question 12: 동시 주문 처리
같은 테이블에서 동시에 여러 주문이 생성될 때의 처리 방식은?

A) 동시 주문 허용 (각각 별도 주문으로 처리)
B) 동시 주문 방지 (이전 주문 처리 완료 후 다음 주문 가능)
C) 동시 주문 허용하되, 짧은 시간 내 중복 주문은 경고 표시
X) Other (please describe after [Answer]: tag below)

[Answer]: A

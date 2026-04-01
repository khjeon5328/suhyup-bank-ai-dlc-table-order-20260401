# Backend NFR Design 질문

backend 유닛의 NFR 설계 패턴 결정을 위해 아래 질문에 답변해 주세요.
각 질문의 `[Answer]:` 태그 뒤에 선택지 알파벳을 입력해 주세요.

---

## Question 1: 프로젝트 구조 패턴
백엔드 코드의 레이어 구조는 어떻게 할까요?

A) 3-Layer (Router → Service → Repository) - 각 레이어 명확 분리
B) 2-Layer (Router → Service) - Service가 직접 DB 접근
C) Clean Architecture (UseCase → Gateway → Repository) - 도메인 중심
X) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 2: 에러 처리 전략
비즈니스 로직 에러를 어떻게 처리할까요?

A) 커스텀 예외 클래스 계층 (AppException → AuthException, OrderException 등)
B) HTTP 예외 직접 사용 (FastAPI HTTPException)
C) Result 패턴 (성공/실패를 반환값으로 처리)
X) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 3: SSE 이벤트 버스 구현
모듈 간 SSE 이벤트 전달 방식은?

A) 인메모리 이벤트 버스 (asyncio.Queue 기반, 단일 인스턴스)
B) 서비스에서 SSEManager 직접 호출
C) Python 이벤트 라이브러리 (blinker 등) 사용
X) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 4: Request ID 추적
요청 추적을 위한 correlation ID 구현 방식은?

A) 미들웨어에서 UUID 생성 → contextvars로 전파 → 모든 로그에 자동 포함
B) 미들웨어에서 UUID 생성 → 함수 파라미터로 전달
C) 클라이언트가 X-Request-ID 헤더로 전송 (없으면 서버 생성)
X) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 5: 의존성 주입 범위
FastAPI Depends를 어느 수준까지 활용할까요?

A) 전체 활용 (DB 세션, 현재 사용자, 서비스 인스턴스 모두 DI)
B) 핵심만 활용 (DB 세션, 현재 사용자만 DI, 서비스는 직접 생성)
C) 최소 활용 (DB 세션만 DI)
X) Other (please describe after [Answer]: tag below)

[Answer]: A

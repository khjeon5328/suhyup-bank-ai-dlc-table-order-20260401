# NFR Requirements 질문 - Unit 1: database

database 유닛의 비기능 요구사항을 확정하기 위해 아래 질문에 답변해 주세요.
각 질문의 `[Answer]:` 태그 뒤에 선택지 알파벳을 입력해 주세요.

---

## Question 1
MySQL 서버 문자셋(Character Set) 설정을 어떻게 할까요?

A) utf8mb4 + utf8mb4_unicode_ci — 이모지 포함 전체 유니코드 지원 (권장)
B) utf8mb3 + utf8_general_ci — 기본 유니코드 (이모지 미지원)
C) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 2
DB 커넥션 풀 사이즈를 어떻게 설정할까요? (동시 접속 500명 기준)

A) 소규모 — pool_size=5, max_overflow=10 (개발/테스트 환경 적합)
B) 중규모 — pool_size=10, max_overflow=20 (MVP 운영 적합)
C) 대규모 — pool_size=20, max_overflow=40 (대규모 트래픽 대비)
D) Other (please describe after [Answer]: tag below)

[Answer]: B

---

## Question 3
MySQL 접속 시 TLS(SSL) 암호화를 어떻게 적용할까요?

A) 필수 적용 — 모든 DB 연결에 TLS 강제 (require_secure_transport=ON)
B) 선택적 적용 — 운영 환경만 TLS, 개발 환경은 비암호화 허용
C) 미적용 — MVP 단계에서는 TLS 없이 진행
D) Other (please describe after [Answer]: tag below)

[Answer]: B

---

## Question 4
Alembic 마이그레이션 실행 방식을 어떻게 할까요?

A) 수동 실행 — 개발자가 CLI로 직접 `alembic upgrade head` 실행
B) 앱 시작 시 자동 — FastAPI 서버 시작 시 자동 마이그레이션 실행
C) CI/CD 파이프라인 — 배포 파이프라인에서 마이그레이션 실행
D) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 5
SQLAlchemy 모델에서 Enum 타입 처리 방식을 어떻게 할까요?

A) Python Enum + MySQL ENUM — SQLAlchemy의 Enum 타입으로 DB에 ENUM 컬럼 생성
B) Python Enum + VARCHAR — Python에서는 Enum 사용, DB에는 문자열로 저장
C) 문자열 상수 — Enum 없이 문자열 상수로 관리
D) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 6
단위 테스트에서 DB 테스트 전략을 어떻게 할까요?

A) SQLite 인메모리 — 테스트 시 SQLite로 대체 (빠르지만 MySQL 호환성 차이 있음)
B) 테스트용 MySQL — 별도 MySQL 인스턴스/DB로 테스트 (정확하지만 환경 필요)
C) Mock/Stub — DB 레이어를 모킹하여 테스트 (빠르지만 통합 검증 부족)
D) Other (please describe after [Answer]: tag below)

[Answer]: B

---

## Question 7
비밀번호 해싱 라이브러리를 어떻게 선택할까요?

A) passlib[bcrypt] — passlib 래퍼 + bcrypt 백엔드 (FastAPI 생태계에서 널리 사용)
B) bcrypt — bcrypt 라이브러리 직접 사용 (의존성 최소화)
C) Other (please describe after [Answer]: tag below)

[Answer]: A


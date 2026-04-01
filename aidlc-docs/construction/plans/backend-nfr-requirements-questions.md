# Backend NFR Requirements 질문

backend 유닛의 비기능 요구사항 및 기술 스택 결정을 위해 아래 질문에 답변해 주세요.
각 질문의 `[Answer]:` 태그 뒤에 선택지 알파벳을 입력해 주세요.

---

## Question 1: API 응답 시간 목표
일반 API 엔드포인트(CRUD 작업)의 목표 응답 시간은?

A) 200ms 이내 (빠른 응답 우선)
B) 500ms 이내 (일반적인 웹 서비스 수준)
C) 1초 이내 (MVP 수준, 최적화는 추후)
X) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 2: 데이터베이스 연결 관리
DB 연결 풀링 전략은 어떻게 할까요?

A) SQLAlchemy async + 기본 연결 풀 (pool_size=5, max_overflow=10)
B) SQLAlchemy async + 대규모 연결 풀 (pool_size=20, max_overflow=40)
C) SQLAlchemy async + 연결 풀 없이 요청마다 새 연결
X) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 3: 로깅 프레임워크
Python 로깅 프레임워크 선택은?

A) Python 표준 logging 모듈 (structlog 래퍼 사용)
B) loguru (간편한 설정, 구조화 로깅)
C) Python 표준 logging 모듈 (기본 설정)
X) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 4: 설정 관리 방식
애플리케이션 설정(DB URL, JWT Secret 등) 관리 방식은?

A) Pydantic Settings (환경 변수 + .env 파일)
B) Python-dotenv + 수동 파싱
C) YAML/TOML 설정 파일
X) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 5: 테스트 프레임워크
단위 테스트 프레임워크 선택은?

A) pytest + pytest-asyncio + httpx (FastAPI TestClient)
B) unittest (Python 표준) + httpx
C) pytest + pytest-asyncio + requests
X) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 6: SSE 동시 연결 수 목표
매장당 SSE 동시 연결 수 목표는?

A) 매장당 최대 50개 (소규모 매장 기준)
B) 매장당 최대 100개 (중규모 매장 기준)
C) 매장당 최대 200개 (대규모 매장 기준)
X) Other (please describe after [Answer]: tag below)

[Answer]: C

---

## Question 7: 데이터 보존 기간
OrderHistory(과거 주문 이력) 데이터 보존 기간은?

A) 무제한 보존
B) 1년 보존 후 자동 삭제
C) 6개월 보존 후 자동 삭제
X) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 8: CORS 허용 정책
CORS(Cross-Origin Resource Sharing) 정책은?

A) 특정 도메인만 허용 (프론트엔드 배포 도메인)
B) 개발 환경에서는 모든 origin 허용, 프로덕션에서는 특정 도메인만
C) 모든 origin 허용 (MVP 단계)
X) Other (please describe after [Answer]: tag below)

[Answer]: B

---

## Question 9: 요청 본문 크기 제한
API 요청 본문(body) 최대 크기는?

A) 1MB (일반 JSON 요청 기준)
B) 5MB (이미지 메타데이터 포함 고려)
C) 10MB (여유 있는 설정)
X) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 10: 마이그레이션 도구
DB 스키마 마이그레이션 도구 선택은?

A) Alembic (SQLAlchemy 공식 마이그레이션 도구)
B) 수동 SQL 스크립트 관리
C) Django-style 자동 마이그레이션 (SQLModel 등)
X) Other (please describe after [Answer]: tag below)

[Answer]: A

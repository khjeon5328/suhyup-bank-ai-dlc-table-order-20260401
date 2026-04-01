# Backend - 기술 스택 결정

---

## 1. 핵심 프레임워크

| 구분 | 선택 | 버전 | 근거 |
|------|------|------|------|
| 웹 프레임워크 | FastAPI | 0.115+ | async 네이티브, 자동 OpenAPI 문서, Pydantic 통합, SSE 지원 |
| Python | Python | 3.11+ | async/await 성능 개선, 타입 힌트 완전 지원 |
| ASGI 서버 | Uvicorn | 0.30+ | FastAPI 공식 권장, HTTP/1.1 + SSE 지원 |

### FastAPI 선택 근거
- async/await 네이티브 → SSE, 동시 접속 500+ 처리에 적합
- Pydantic v2 통합 → 입력 검증 자동화 (SECURITY-05)
- 자동 OpenAPI/Swagger 문서 생성
- Dependency Injection 내장 → 인증/인가 미들웨어 구현 용이
- 높은 성능 (Node.js/Go 수준 벤치마크)

---

## 2. 데이터베이스 레이어

| 구분 | 선택 | 버전 | 근거 |
|------|------|------|------|
| ORM | SQLAlchemy | 2.0+ | async 지원, 성숙한 생태계, Alembic 통합 |
| Async 드라이버 | aiomysql | 0.2+ | MySQL async 연결, SQLAlchemy async 호환 |
| 마이그레이션 | Alembic | 1.13+ | SQLAlchemy 공식, 자동 마이그레이션 생성 |
| DB | MySQL | 8.0+ | 요구사항 명시, 트랜잭션/인덱스 지원 |

---

## 3. 인증/보안

| 구분 | 선택 | 버전 | 근거 |
|------|------|------|------|
| JWT | PyJWT | 2.8+ | 경량, HS256 지원, 널리 사용 |
| 비밀번호 해싱 | bcrypt (passlib) | 1.7+ | adaptive algorithm, SECURITY-12 준수 |
| CORS | FastAPI CORSMiddleware | 내장 | 환경별 origin 설정 |
| Rate Limiting | slowapi | 0.1+ | FastAPI 호환, IP/키 기반 제한 |

---

## 4. 로깅/모니터링

| 구분 | 선택 | 버전 | 근거 |
|------|------|------|------|
| 로깅 | structlog | 24.0+ | JSON 구조화 로깅, request_id 자동 바인딩 |
| 로깅 백엔드 | Python logging | 표준 | structlog → logging 파이프라인 |

---

## 5. 설정/유틸리티

| 구분 | 선택 | 버전 | 근거 |
|------|------|------|------|
| 설정 관리 | pydantic-settings | 2.0+ | 환경 변수 + .env, 타입 검증 |
| S3 클라이언트 | boto3 | 1.34+ | AWS S3 presigned URL 생성 |
| 날짜/시간 | Python datetime + zoneinfo | 표준 | UTC 기준, 타임존 처리 |

---

## 6. 테스트

| 구분 | 선택 | 버전 | 근거 |
|------|------|------|------|
| 테스트 프레임워크 | pytest | 8.0+ | Python 표준 테스트 도구 |
| Async 테스트 | pytest-asyncio | 0.23+ | async 테스트 케이스 지원 |
| HTTP 클라이언트 | httpx | 0.27+ | FastAPI AsyncClient, async 지원 |
| 커버리지 | pytest-cov | 5.0+ | 코드 커버리지 측정 |

---

## 7. 의존성 요약 (requirements.txt)

```
# Core
fastapi>=0.115.0
uvicorn[standard]>=0.30.0
python-multipart>=0.0.9

# Database
sqlalchemy[asyncio]>=2.0.0
aiomysql>=0.2.0
alembic>=1.13.0

# Auth & Security
PyJWT>=2.8.0
passlib[bcrypt]>=1.7.0
slowapi>=0.1.9

# Logging
structlog>=24.0.0

# Settings
pydantic-settings>=2.0.0

# Cloud
boto3>=1.34.0

# Testing (dev)
pytest>=8.0.0
pytest-asyncio>=0.23.0
httpx>=0.27.0
pytest-cov>=5.0.0
```

---

## 8. 대안 비교

### 웹 프레임워크: FastAPI vs Django vs Flask

| 기준 | FastAPI | Django | Flask |
|------|---------|--------|-------|
| Async 네이티브 | O | 부분적 (ASGI) | X |
| 자동 API 문서 | O (OpenAPI) | X (DRF 필요) | X |
| 입력 검증 | Pydantic 내장 | Serializer | 수동 |
| SSE 지원 | 네이티브 | 제한적 | 제한적 |
| 성능 | 높음 | 중간 | 중간 |
| 학습 곡선 | 낮음 | 높음 | 낮음 |
| 선택 이유 | **async + SSE + 자동 문서 + 성능** | - | - |

### ORM: SQLAlchemy vs Django ORM vs Tortoise

| 기준 | SQLAlchemy 2.0 | Django ORM | Tortoise |
|------|---------------|------------|----------|
| Async 지원 | O (네이티브) | 부분적 | O |
| 마이그레이션 | Alembic | 내장 | Aerich |
| 생태계 성숙도 | 매우 높음 | 높음 | 낮음 |
| FastAPI 호환 | 완벽 | 불편 | 좋음 |
| 선택 이유 | **async + 성숙도 + Alembic** | - | - |

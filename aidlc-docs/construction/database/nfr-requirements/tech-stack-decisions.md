# Tech Stack Decisions - Unit 1: database

---

## 1. 핵심 의존성

| 패키지 | 버전 | 용도 | 선택 근거 |
|--------|------|------|-----------|
| sqlalchemy | >=2.0,<3.0 | ORM, 모델 정의 | 비동기 지원, Python 생태계 표준 ORM |
| alembic | >=1.13,<2.0 | DB 마이그레이션 | SQLAlchemy 공식 마이그레이션 도구 |
| asyncmy | >=0.2,<1.0 | MySQL 비동기 드라이버 | SQLAlchemy async 엔진 호환, 순수 Python |
| pydantic | >=2.0,<3.0 | 스키마 검증, DTO | FastAPI 기본 통합, 타입 안전성 |
| passlib[bcrypt] | >=1.7,<2.0 | 비밀번호 해싱 | bcrypt 래퍼, FastAPI 생태계 표준 |
| python-dotenv | >=1.0,<2.0 | 환경 변수 로드 | .env 파일 기반 설정 관리 |

## 2. 테스트 의존성

| 패키지 | 버전 | 용도 |
|--------|------|------|
| pytest | >=8.0,<9.0 | 테스트 프레임워크 |
| pytest-asyncio | >=0.23,<1.0 | 비동기 테스트 지원 |

## 3. 드라이버 선택 근거

### asyncmy vs aiomysql
- **asyncmy 선택**: 순수 Python 구현으로 설치가 간편하고, SQLAlchemy 2.0 async와 호환성이 좋음
- **aiomysql 미선택**: PyMySQL 기반이라 일부 SQLAlchemy 2.0 기능과 호환 이슈 보고됨

### passlib vs bcrypt 직접 사용
- **passlib 선택**: CryptContext로 해싱/검증 래핑, 알고리즘 변경 용이, FastAPI 공식 문서 권장
- **bcrypt 직접 미선택**: 보일러플레이트 코드 증가, 알고리즘 전환 시 코드 수정 필요

---

## 4. MySQL 설정

| 설정 | 값 | 이유 |
|------|-----|------|
| character_set_server | utf8mb4 | 이모지 포함 전체 유니코드 |
| collation_server | utf8mb4_unicode_ci | 유니코드 정렬 |
| default_storage_engine | InnoDB | 트랜잭션, FK 지원 |
| require_secure_transport | ON (운영) / OFF (개발) | SECURITY-01 준수 |

---

## 5. Python 버전
- **Python 3.11+**: SQLAlchemy 2.0 async, 타입 힌트, 성능 개선

---

## 6. 환경 변수 구조

```
# DB 연결
DB_HOST=localhost
DB_PORT=3306
DB_USER=tableorder
DB_PASSWORD=<secret>
DB_NAME=tableorder

# DB 옵션
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
DB_ECHO=false

# TLS (운영 환경)
DB_SSL_MODE=REQUIRED
DB_SSL_CA=/path/to/ca.pem

# 환경 구분
ENVIRONMENT=development
```

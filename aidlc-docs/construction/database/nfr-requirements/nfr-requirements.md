# NFR Requirements - Unit 1: database

---

## 1. 성능 요구사항

### NFR-DB-01: 커넥션 풀 설정
- pool_size: 10 (기본 유지 커넥션)
- max_overflow: 20 (최대 추가 커넥션)
- pool_timeout: 30초 (커넥션 대기 타임아웃)
- pool_recycle: 3600초 (1시간마다 커넥션 재생성, MySQL wait_timeout 대응)
- pool_pre_ping: True (사용 전 커넥션 유효성 검사)

### NFR-DB-02: 쿼리 최적화
- 모든 FK 컬럼에 인덱스 적용
- 자주 사용되는 복합 쿼리 패턴에 복합 인덱스 적용:
  - `(store_code, table_no, ended_at)` — 활성 세션 조회
  - `(store_code, archived_at, created_at)` — 현재/과거 주문 조회
  - `(store_code, category_id, sort_order)` — 메뉴 목록 조회
- Lazy loading 기본, 필요 시 joinedload/selectinload 명시적 사용
- N+1 쿼리 방지를 위한 관계 로딩 전략 문서화

### NFR-DB-03: 문자셋 및 콜레이션
- 문자셋: utf8mb4 (이모지 포함 전체 유니코드)
- 콜레이션: utf8mb4_unicode_ci (유니코드 정렬)
- DB, 테이블, 컬럼 레벨 모두 일관 적용

---

## 2. 보안 요구사항

### NFR-DB-04: 전송 암호화 (SECURITY-01 준수)
- 운영 환경: TLS 1.2+ 필수 (MySQL require_secure_transport=ON)
- 개발 환경: TLS 선택적 (환경 변수로 분기)
- 연결 문자열에 ssl_mode 파라미터 지원

### NFR-DB-05: 비밀번호 해싱 (SECURITY-12 준수)
- 라이브러리: passlib[bcrypt]
- 알고리즘: bcrypt (adaptive hashing)
- CryptContext 설정: schemes=["bcrypt"], deprecated="auto"
- 관리자 비밀번호, 테이블 PIN 모두 bcrypt 해싱 적용

### NFR-DB-06: SQL Injection 방지 (SECURITY-05 준수)
- SQLAlchemy ORM 사용으로 파라미터 바인딩 자동 적용
- Raw SQL 사용 금지 (불가피한 경우 text() + bindparams 필수)
- 사용자 입력값 직접 쿼리 문자열 결합 절대 금지

### NFR-DB-07: 민감 데이터 보호 (SECURITY-03 준수)
- 비밀번호 해시는 API 응답에 절대 포함하지 않음
- Pydantic Response 스키마에서 password_hash 필드 제외
- 로그에 비밀번호, 토큰, PIN 출력 금지

### NFR-DB-08: 하드코딩 금지 (SECURITY-12 준수)
- DB 접속 정보 (host, port, user, password)는 환경 변수로 관리
- 시드 데이터의 기본 비밀번호는 개발 환경 전용, 운영 배포 시 변경 필수
- 소스 코드에 비밀번호, API 키 등 하드코딩 금지

---

## 3. 가용성 요구사항

### NFR-DB-09: 마이그레이션 안전성
- Alembic 수동 실행 (개발자 CLI)
- 마이그레이션 전 백업 권장 (운영 환경)
- 다운그레이드 스크립트 포함 (rollback 가능)
- 마이그레이션 파일에 변경 내용 주석 필수

### NFR-DB-10: 에러 처리 (SECURITY-15 준수)
- DB 연결 실패 시 명확한 에러 메시지 (내부 로그용)
- 사용자에게는 일반적인 에러 메시지만 노출
- 커넥션 풀 고갈 시 graceful degradation (타임아웃 후 503 응답)
- 트랜잭션 실패 시 자동 롤백

### NFR-DB-11: 데이터 무결성
- 외래 키 제약조건 활성화 (InnoDB)
- CHECK 제약조건 적용 (price >= 0, quantity > 0 등)
- 트랜잭션 격리 수준: READ COMMITTED (기본)
- 이용 완료 처리(세션 종료 + 주문 아카이브)는 단일 트랜잭션으로 처리

---

## 4. 유지보수성 요구사항

### NFR-DB-12: 코드 구조
- 모델, 스키마, 시드를 명확히 분리된 모듈로 구성
- Base 모델에 공통 필드(created_at, updated_at) Mixin 적용
- 소프트 삭제 Mixin 별도 정의 (Menu, User에 적용)

### NFR-DB-13: 테스트 전략
- 테스트용 MySQL 인스턴스 사용 (Docker 컨테이너 권장)
- 테스트 DB는 각 테스트 세션마다 초기화
- 모델 CRUD 테스트, 제약조건 테스트, 관계 테스트 포함
- pytest + pytest-asyncio 사용

### NFR-DB-14: 의존성 관리 (SECURITY-10 준수)
- requirements.txt에 정확한 버전 핀닝
- 사용하지 않는 의존성 제거
- 공식 PyPI 레지스트리에서만 패키지 설치

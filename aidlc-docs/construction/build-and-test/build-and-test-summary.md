# Build and Test Summary - 테이블오더 서비스

## 프로젝트 현황

| 유닛 | 담당 | 코드 생성 | 연동 검증 |
|------|------|----------|----------|
| Unit 1: database | 지현 | ✅ 완료 | ✅ |
| Unit 2: backend | 소윤 | ✅ 완료 | ✅ |
| Unit 3: frontend-customer | 국현 | ✅ 완료 | ✅ |
| Unit 4: frontend-admin | 수민 | ✅ 완료 | ✅ |

## 연동 검증 결과

| 연동 | 상태 | 수정 내용 |
|------|------|----------|
| Unit 1 ↔ Unit 2 | ✅ | store_code 기반 모델 참조 확인 |
| Unit 2 ↔ Unit 3 | ✅ | store_code/table_no 기반 API 경로 통일, 로그인 응답 구조 맞춤, 불필요 필드 제거 |
| Unit 2 ↔ Unit 4 | ✅ | store_code/table_no 기반 API 경로 통일, 역할 기반 접근 제어 확인 |
| SSE 인증 | ✅ | 쿼리 파라미터 토큰 인증 지원 추가 (EventSource 제약) |

## 빌드 사전 요구사항

| 도구 | 버전 | 용도 |
|------|------|------|
| Python | 3.11+ | backend, database |
| Node.js | 18+ | frontend-customer, frontend-admin |
| MySQL | 8.0+ | 데이터베이스 |
| npm | 9+ | 프론트엔드 패키지 관리 |

## 빌드 순서

```
1. MySQL DB 생성
2. database: pip install → alembic upgrade head → seed
3. backend: pip install → uvicorn 실행
4. frontend-customer: npm install → npm run build
5. frontend-admin: npm install → npm run build
```

## 테스트 실행

### 단위 테스트
```bash
# Unit 1: database
cd table-order/database && pytest tests/ -v

# Unit 2: backend
cd backend && pytest tests/ -v

# Unit 3: frontend-customer
cd frontend-customer && npm run test

# Unit 4: frontend-admin
cd frontend-admin && npm run test
```

### 통합 테스트 시나리오 (7개)
1. 테이블 로그인 (Unit 3 → 2 → 1)
2. 메뉴 조회 (Unit 3 → 2 → 1)
3. 주문 생성 → 실시간 모니터링 (Unit 3 → 2 → 4)
4. 주문 상태 변경 → 고객 실시간 (Unit 4 → 2 → 3)
5. 테이블 이용 완료 (Unit 4 → 2 → 1)
6. 역할 기반 접근 제어 (Unit 4 → 2)
7. 브루트포스 방지 (Unit 4 → 2)

### 성능 테스트 시나리오 (4개)
1. 메뉴 조회 부하 (500명 동시)
2. 주문 생성 부하 (200명 동시)
3. SSE 동시 연결 (500개)
4. 혼합 시나리오 (10분)

## 현재 상태
- **빌드**: ⏳ 실행 환경 미설치 (Python, Node.js 필요)
- **단위 테스트**: ⏳ 빌드 환경 설치 후 실행 필요
- **통합 테스트**: ⏳ 전체 서비스 기동 후 수동 검증 필요
- **성능 테스트**: ⏳ k6 또는 JMeter 설치 후 실행 필요

## 다음 단계
1. Python 3.11+, Node.js 18+ 설치
2. 각 유닛 빌드 및 단위 테스트 실행
3. 전체 서비스 기동 후 통합 테스트 수행
4. 성능 테스트 수행 (선택)

## 생성된 지침서
- `build-instructions.md` — 빌드 순서 및 환경 설정
- `unit-test-instructions.md` — 유닛별 테스트 실행
- `integration-test-instructions.md` — 7개 통합 테스트 시나리오
- `performance-test-instructions.md` — 4개 성능 테스트 시나리오

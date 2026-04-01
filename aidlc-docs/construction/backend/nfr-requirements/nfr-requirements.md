# Backend - NFR 요구사항 정의서

---

## 1. 성능 요구사항

### NFR-PERF-01: API 응답 시간
| 구분 | 목표 | 측정 기준 |
|------|------|----------|
| 일반 CRUD API | 200ms 이내 (p95) | 서버 처리 시간 (네트워크 제외) |
| 주문 생성 API | 300ms 이내 (p95) | 트랜잭션 + SSE 발행 포함 |
| 메뉴 목록 조회 | 150ms 이내 (p95) | 카테고리 포함 조회 |
| SSE 이벤트 전달 | 2초 이내 | 이벤트 발생 → 클라이언트 수신 |

### NFR-PERF-02: 처리량
| 구분 | 목표 |
|------|------|
| 동시 접속 | 500명 이상 |
| 초당 요청 수 (RPS) | 100 RPS 이상 |
| SSE 동시 연결 | 매장당 최대 200개, 전체 4,000개 (20매장) |

### NFR-PERF-03: 데이터베이스 성능
| 구분 | 설정 |
|------|------|
| 연결 풀 크기 | pool_size=5, max_overflow=10 |
| 연결 타임아웃 | 30초 |
| 쿼리 타임아웃 | 10초 |
| 인덱스 | domain-entities.md 인덱스 전략 참조 |

---

## 2. 확장성 요구사항

### NFR-SCALE-01: 수평 확장
- 단일 서버 기준 500명 동시 접속 지원
- Stateless API 설계 (JWT 기반, 서버 세션 없음)
- SSE 연결은 서버 인스턴스에 바인딩 (단일 인스턴스 기준 설계)
- 추후 Redis Pub/Sub 등으로 멀티 인스턴스 SSE 확장 가능

### NFR-SCALE-02: 데이터 증가
| 구분 | 예상 규모 |
|------|----------|
| 매장 수 | 20개 이상 |
| 매장당 테이블 | 최대 50개 |
| 일일 주문 수 (매장당) | 최대 500건 |
| OrderHistory 보존 | 무제한 |

---

## 3. 가용성 요구사항

### NFR-AVAIL-01: 에러 처리
- 글로벌 예외 핸들러로 모든 미처리 예외 포착
- 에러 시 generic 메시지 반환 (내부 정보 노출 금지)
- DB 연결 실패 시 graceful degradation (재시도 로직)
- SSE 연결 끊김 시 클라이언트 자동 재연결 + 전체 데이터 새로고침

### NFR-AVAIL-02: 리소스 정리
- DB 연결: async context manager로 자동 반환
- SSE 연결: 클라이언트 disconnect 감지 시 연결 풀에서 제거
- 파일 핸들: try/finally 패턴으로 정리

---

## 4. 보안 요구사항 (SECURITY 규칙 매핑)

### NFR-SEC-01: 데이터 보호 (SECURITY-01)
| 항목 | 구현 |
|------|------|
| 전송 암호화 | HTTPS 강제 (TLS 1.2+) |
| DB 연결 암호화 | MySQL TLS 연결 |
| 비밀번호 저장 | bcrypt 해싱 (adaptive algorithm) |

### NFR-SEC-02: 로깅 (SECURITY-02, SECURITY-03)
| 항목 | 구현 |
|------|------|
| 프레임워크 | Python logging + structlog |
| 로그 형식 | JSON 구조화 (timestamp, request_id, level, message) |
| 민감 데이터 | 비밀번호, 토큰, PII 로깅 금지 |
| 보존 기간 | 최소 90일 |

### NFR-SEC-03: HTTP 보안 헤더 (SECURITY-04)
| 헤더 | 값 |
|------|-----|
| Content-Security-Policy | default-src 'self' |
| Strict-Transport-Security | max-age=31536000; includeSubDomains |
| X-Content-Type-Options | nosniff |
| X-Frame-Options | DENY |
| Referrer-Policy | strict-origin-when-cross-origin |

### NFR-SEC-04: 입력 검증 (SECURITY-05)
| 항목 | 구현 |
|------|------|
| 검증 라이브러리 | Pydantic v2 (FastAPI 내장) |
| 문자열 최대 길이 | 필드별 명시적 제한 |
| 요청 본문 크기 | 1MB 제한 |
| SQL Injection 방지 | SQLAlchemy ORM (파라미터화 쿼리) |
| XSS 방지 | 입력값 이스케이프 처리 |

### NFR-SEC-05: 접근 제어 (SECURITY-06, SECURITY-08)
| 항목 | 구현 |
|------|------|
| 인증 | JWT 토큰 (모든 보호 엔드포인트) |
| 인가 | 역할 기반 (owner/manager/table) |
| 객체 수준 인가 | store_id 소유권 검증 (IDOR 방지) |
| CORS | 환경별 분리 (개발: 전체, 프로덕션: 특정 도메인) |
| 기본 정책 | Deny by default |

### NFR-SEC-06: Rate Limiting (SECURITY-11)
| 엔드포인트 | 제한 |
|-----------|------|
| POST /auth/login/* | IP: 15분당 20회, 계정: 15분당 5회 |
| 일반 API | 분당 60회 (인증된 사용자) |
| SSE 연결 | 매장당 200개 제한 |

### NFR-SEC-07: 인증 관리 (SECURITY-12)
| 항목 | 구현 |
|------|------|
| 비밀번호 해싱 | bcrypt (adaptive) |
| 비밀번호 정책 | 최소 8자 |
| 세션 만료 | 관리자 16시간, 테이블 무제한 |
| 브루트포스 방지 | IP + 계정 복합 잠금 |
| 하드코딩 금지 | Pydantic Settings + 환경 변수 |

### NFR-SEC-08: 예외 처리 (SECURITY-15)
| 항목 | 구현 |
|------|------|
| 글로벌 핸들러 | FastAPI exception_handler |
| 에러 응답 | generic 메시지 (스택 트레이스 노출 금지) |
| Fail closed | 에러 시 접근 거부 |
| 리소스 정리 | async context manager / try-finally |

---

## 5. 신뢰성 요구사항

### NFR-REL-01: 데이터 무결성
- 주문 생성: DB 트랜잭션으로 Order + OrderItem 원자적 생성
- 이용 완료: 아카이브 + 세션 종료 + 새 세션 생성을 단일 트랜잭션
- 주문 번호: SELECT FOR UPDATE로 동시성 충돌 방지

### NFR-REL-02: 멱등성
- 주문 생성: 중복 요청 시 별도 주문으로 처리 (동시 주문 허용)
- 상태 변경: 동일 상태로의 변경 요청은 무시 (200 반환)

---

## 6. 유지보수성 요구사항

### NFR-MAINT-01: 코드 구조
- 레이어 분리: Router → Service → Repository
- 의존성 주입: FastAPI Depends
- 설정 관리: Pydantic Settings (환경별 분리)

### NFR-MAINT-02: 테스트
| 구분 | 도구 |
|------|------|
| 프레임워크 | pytest + pytest-asyncio |
| HTTP 클라이언트 | httpx (AsyncClient) |
| DB 테스트 | SQLite in-memory 또는 테스트 MySQL |
| 커버리지 목표 | 서비스 레이어 80% 이상 |

### NFR-MAINT-03: 마이그레이션
- 도구: Alembic (database 유닛과 공유)
- 버전 관리: Git 커밋과 함께 마이그레이션 파일 관리

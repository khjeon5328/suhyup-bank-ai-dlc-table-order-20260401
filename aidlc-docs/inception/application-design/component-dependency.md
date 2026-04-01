# 테이블오더 서비스 - 컴포넌트 의존성

---

## 의존성 매트릭스

| 컴포넌트 | 의존 대상 | 관계 유형 |
|----------|----------|-----------|
| FE-CUSTOMER | BE-AUTH, BE-MENU, BE-ORDER, BE-SSE | HTTP REST, SSE |
| FE-ADMIN | BE-AUTH, BE-MENU, BE-ORDER, BE-TABLE, BE-USER, BE-IMAGE, BE-SSE | HTTP REST, SSE |
| BE-AUTH | DB-MYSQL | 데이터 접근 |
| BE-STORE | DB-MYSQL | 데이터 접근 |
| BE-TABLE | DB-MYSQL, BE-ORDER | 데이터 접근, 서비스 호출 |
| BE-MENU | DB-MYSQL, STORAGE-S3 | 데이터 접근, 파일 저장 |
| BE-ORDER | DB-MYSQL, BE-SSE | 데이터 접근, 이벤트 발행 |
| BE-SSE | - | 독립 (이벤트 수신만) |
| BE-USER | DB-MYSQL, BE-AUTH | 데이터 접근, 비밀번호 해싱 |
| BE-IMAGE | STORAGE-S3 | 파일 저장 |

---

## 통신 패턴

### 프론트엔드 ↔ 백엔드
- **프로토콜**: HTTPS REST API
- **인증**: JWT Bearer Token (Authorization 헤더)
- **데이터 형식**: JSON
- **실시간**: Server-Sent Events (SSE)

### 백엔드 ↔ 데이터베이스
- **프로토콜**: MySQL 프로토콜 (TLS)
- **ORM**: SQLAlchemy (async)
- **연결 풀링**: 비동기 커넥션 풀

### 백엔드 ↔ 클라우드 스토리지
- **프로토콜**: HTTPS (S3 API)
- **인증**: IAM 자격 증명
- **방식**: Presigned URL (클라이언트 직접 업로드)

---

## 데이터 흐름

### 주문 생성 흐름
```
고객 태블릿 → POST /orders → BE-ORDER → DB 저장
                                    → BE-SSE → 관리자 대시보드 (SSE)
```

### 주문 상태 변경 흐름
```
관리자 → PATCH /orders/{id}/status → BE-ORDER → DB 업데이트
                                          → BE-SSE → 고객 태블릿 (SSE)
                                          → BE-SSE → 관리자 대시보드 (SSE)
```

### 이용 완료 흐름
```
관리자 → POST /tables/{id}/session/end → BE-TABLE → BE-ORDER (아카이브)
                                                  → DB 업데이트
                                                  → BE-SSE → 고객 태블릿 (SSE)
```

---

## 계층 구조

```
+-------------------------------------------+
|          Presentation Layer               |
|  FE-CUSTOMER (Vue.js) | FE-ADMIN (Vue.js)|
+-------------------------------------------+
                    |
+-------------------------------------------+
|            API Layer (FastAPI)             |
|  Routers + Middleware (Auth, CORS, etc.)  |
+-------------------------------------------+
                    |
+-------------------------------------------+
|           Service Layer                    |
|  SVC-AUTH | SVC-ORDER | SVC-TABLE | ...  |
+-------------------------------------------+
                    |
+-------------------------------------------+
|         Data Access Layer (DAL)           |
|  SQLAlchemy Models + Repositories         |
+-------------------------------------------+
                    |
+-------------------------------------------+
|          Infrastructure Layer             |
|  MySQL | S3 | SSE Connection Manager      |
+-------------------------------------------+
```

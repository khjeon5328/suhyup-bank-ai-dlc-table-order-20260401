# 테이블오더 서비스 - 서비스 레이어 정의

---

## 서비스 아키텍처 개요

```
+------------------+     +-------------------+
| FE-CUSTOMER      |     | FE-ADMIN          |
| (Vue.js SPA)     |     | (Vue.js SPA)      |
+--------+---------+     +---------+---------+
         |                         |
         |      HTTPS/REST         |
         +------------+------------+
                      |
              +-------v--------+
              | FastAPI Server |
              | (API Gateway)  |
              +-------+--------+
                      |
         +------------+------------+
         |            |            |
   +-----v----+ +----v-----+ +---v------+
   | Auth     | | Business | | SSE      |
   | Service  | | Services | | Service  |
   +-----+----+ +----+-----+ +---+------+
         |            |            |
         +------------+------------+
                      |
              +-------v--------+
              | Data Access    |
              | Layer (DAL)    |
              +-------+--------+
                      |
              +-------v--------+
              |    MySQL       |
              +----------------+
```

---

## 서비스 정의

### SVC-AUTH: 인증 서비스
**책임**: 인증/인가 처리 전담
**오케스트레이션**:
- BE-AUTH 모듈을 사용하여 로그인/토큰 검증 수행
- FastAPI 미들웨어로 모든 요청에 토큰 검증 적용
- 역할 기반 라우트 가드 (Dependency Injection)

### SVC-STORE: 매장 서비스
**책임**: 매장 정보 관리
**오케스트레이션**:
- BE-STORE 모듈을 통한 매장 데이터 접근

### SVC-TABLE: 테이블 서비스
**책임**: 테이블 설정 및 세션 관리
**오케스트레이션**:
- BE-TABLE로 테이블 CRUD 및 세션 관리
- BE-ORDER의 `archive_session_orders`를 호출하여 이용 완료 시 주문 아카이브
- BE-SSE로 테이블 상태 변경 이벤트 발행

### SVC-MENU: 메뉴 서비스
**책임**: 메뉴 CRUD 및 이미지 관리
**오케스트레이션**:
- BE-MENU로 메뉴 데이터 관리
- BE-IMAGE로 이미지 업로드 URL 생성

### SVC-ORDER: 주문 서비스
**책임**: 주문 생성, 상태 관리, 이력 관리
**오케스트레이션**:
- BE-ORDER로 주문 CRUD
- BE-TABLE의 세션 정보 참조 (현재 세션 주문 필터링)
- BE-SSE로 주문 이벤트 브로드캐스트 (생성/상태변경/삭제)

### SVC-SSE: 실시간 이벤트 서비스
**책임**: SSE 연결 관리 및 이벤트 배포
**오케스트레이션**:
- BE-SSE로 연결 관리
- 매장별 이벤트 채널 분리
- 관리자/테이블별 이벤트 필터링

### SVC-USER: 사용자 서비스
**책임**: 관리자 계정 관리
**오케스트레이션**:
- BE-USER로 계정 CRUD
- BE-AUTH로 비밀번호 해싱

---

## API 라우터 구조

```
/api/v1/
├── /auth/
│   ├── POST /login/admin          # 관리자 로그인
│   └── POST /login/table          # 테이블 로그인
├── /stores/{store_id}/
│   ├── GET /                       # 매장 정보
│   ├── /tables/
│   │   ├── GET /                   # 테이블 목록
│   │   ├── POST /                  # 테이블 설정
│   │   ├── GET /{table_id}         # 테이블 상세
│   │   ├── POST /{table_id}/session/end  # 이용 완료
│   │   └── GET /{table_id}/history # 과거 내역
│   ├── /menus/
│   │   ├── GET /                   # 메뉴 목록
│   │   ├── POST /                  # 메뉴 등록 (점주)
│   │   ├── GET /categories         # 카테고리 목록
│   │   ├── GET /{menu_id}          # 메뉴 상세
│   │   ├── PUT /{menu_id}          # 메뉴 수정 (점주)
│   │   ├── DELETE /{menu_id}       # 메뉴 삭제 (점주)
│   │   └── PUT /order              # 메뉴 순서 변경 (점주)
│   ├── /orders/
│   │   ├── GET /                   # 주문 목록
│   │   ├── POST /                  # 주문 생성
│   │   ├── GET /{order_id}         # 주문 상세
│   │   ├── PATCH /{order_id}/status # 주문 상태 변경
│   │   └── DELETE /{order_id}      # 주문 삭제 (점주)
│   ├── /users/
│   │   ├── GET /                   # 계정 목록 (점주)
│   │   ├── POST /                  # 계정 생성 (점주)
│   │   ├── PUT /{user_id}          # 계정 수정 (점주)
│   │   └── DELETE /{user_id}       # 계정 삭제 (점주)
│   ├── /images/
│   │   └── POST /presigned-url     # 업로드 URL 생성 (점주)
│   └── /events/
│       ├── GET /admin              # 관리자 SSE 스트림
│       └── GET /table/{table_id}   # 테이블 SSE 스트림
```

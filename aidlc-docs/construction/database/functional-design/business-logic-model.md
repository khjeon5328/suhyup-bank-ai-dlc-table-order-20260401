# Unit 1: database - 비즈니스 로직 모델

> 담당자: 지현

---

## 1. 시드 데이터 전략

### 초기 데이터 구성

**매장 시드 데이터**:
- 1개 샘플 매장 (code: "STORE001")
- 점주 계정 1개 (username: "owner", role: "owner")
- 매니저 계정 1개 (username: "manager", role: "manager")

**테이블 시드 데이터**:
- 5개 테이블 (table_no: 1~5)
- 각 테이블 기본 비밀번호 설정

**메뉴 시드 데이터**:
- 3개 카테고리 (메인, 사이드, 음료)
- 카테고리당 3~4개 메뉴 (총 10개)
- 샘플 이미지 URL 포함

### 시드 실행 방식
```
1. Alembic 마이그레이션으로 스키마 생성
2. seed 스크립트로 초기 데이터 삽입
3. 비밀번호는 bcrypt 해싱 후 저장
4. 멱등성 보장 (이미 존재하면 건너뜀)
```

---

## 2. Pydantic 스키마 구조

### 요청/응답 스키마 분류

**Base 스키마**: 공통 필드 정의
**Create 스키마**: 생성 요청용 (id 제외)
**Update 스키마**: 수정 요청용 (모든 필드 Optional)
**Response 스키마**: 응답용 (id, timestamps 포함)

### 주요 스키마 목록

| 엔티티 | Create | Update | Response | List |
|--------|--------|--------|----------|------|
| Store | - | - | StoreResponse | - |
| User | UserCreate | UserUpdate | UserResponse | UserListResponse |
| Table | TableCreate | - | TableResponse | TableSummaryResponse |
| Session | - | - | SessionResponse | - |
| Category | CategoryCreate | - | CategoryResponse | - |
| Menu | MenuCreate | MenuUpdate | MenuResponse | MenuListResponse |
| Order | OrderCreate | - | OrderResponse | OrderListResponse |
| OrderItem | OrderItemCreate | - | OrderItemResponse | - |

### 인증 관련 스키마

| 스키마 | 용도 |
|--------|------|
| AdminLoginRequest | 관리자 로그인 요청 (store_code, username, password) |
| TableLoginRequest | 테이블 로그인 요청 (store_code, table_no, password) |
| TokenResponse | JWT 토큰 응답 (access_token, token_type, expires_in) |
| TokenPayload | JWT 페이로드 (user_id/table_id, store_id, role, exp) |

---

## 3. DB 연결 설정

### 비동기 연결 풀
```
- Engine: AsyncEngine (aiomysql)
- Session: AsyncSession
- Pool Size: 10 (기본)
- Max Overflow: 20
- Pool Recycle: 3600초 (1시간)
- Echo: False (프로덕션)
```

### 환경 변수
```
DATABASE_URL=mysql+aiomysql://user:password@host:3306/table_order
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20
```

---

## 4. 마이그레이션 전략

### Alembic 설정
- 비동기 마이그레이션 지원
- 자동 마이그레이션 생성 (autogenerate)
- 마이그레이션 파일 버전 관리

### 초기 마이그레이션
```
001_initial_schema.py
  - Store 테이블 생성
  - User 테이블 생성
  - RestaurantTable 테이블 생성
  - TableSession 테이블 생성
  - Category 테이블 생성
  - Menu 테이블 생성
  - Order 테이블 생성
  - OrderItem 테이블 생성
  - 인덱스 생성
  - 외래키 제약조건 설정
```

# 🍽 테이블오더 (Table Order)

디지털 주문 시스템을 통해 고객에게는 편리한 주문 경험을, 매장 운영자에게는 효율적인 운영 환경을 제공하는 테이블오더 플랫폼입니다.

## 서비스 소개

고객은 테이블에 설치된 태블릿으로 메뉴를 탐색하고 주문하며, 매장 관리자는 실시간 대시보드에서 주문을 모니터링하고 관리합니다.

```
고객 태블릿 ──주문──▶ FastAPI 서버 ◀──모니터링── 관리자 대시보드
                          │
                    ┌─────┴─────┐
                    ▼           ▼
                  MySQL        S3
```

## 기술 스택

| 구분 | 기술 |
|------|------|
| Backend | Python FastAPI, SQLAlchemy (async), Alembic |
| Frontend | Vue.js 3, Pinia, Vue Router, Vite |
| Database | MySQL |
| 실시간 통신 | Server-Sent Events (SSE) |
| 이미지 저장 | AWS S3 (Presigned URL) |
| 인증 | JWT + bcrypt |

## 프로젝트 구조

```
table-order/
├── database/                 # DB 모델, 스키마, 마이그레이션, 시드 데이터
├── backend/                  # FastAPI API 서버
├── frontend-customer/        # 고객용 주문 웹앱 (Vue.js)
├── frontend-admin/           # 관리자용 대시보드 (Vue.js)
└── aidlc-docs/               # 설계 문서 (AI-DLC)
```

## 주요 기능

### 고객용
- 태블릿 자동 로그인 (1회 설정 후 무제한 세션)
- 카테고리별 메뉴 조회 및 상세 보기
- 장바구니 관리 (로컬 저장, 새로고침 유지)
- 주문 생성 및 실시간 상태 확인 (SSE)
- 주문 내역 조회 (현재 세션)

### 관리자용
- JWT 기반 로그인 (16시간 세션)
- 실시간 주문 모니터링 대시보드 (SSE, 2초 이내)
- 주문 상태 변경 (대기중 → 준비중 → 완료)
- 테이블 관리 (설정, 이용 완료, 과거 내역)
- 메뉴 CRUD 및 이미지 업로드
- 역할 기반 권한 (점주: 전체 권한 / 매니저: 제한 권한)

## 시작하기

### 사전 요구사항
- Python 3.11+
- Node.js 18+
- MySQL 8.0+

### 고객용 프론트엔드 실행
```bash
cd frontend-customer
cp .env.example .env
npm install
npm run dev
```

### 테스트 실행
```bash
cd frontend-customer
npm run test
```

## 팀

| 담당 | 유닛 | 역할 |
|------|------|------|
| 지현 | database | DB 모델, 스키마, 마이그레이션, 시드 데이터 |
| 소윤 | backend | FastAPI API 서버, 비즈니스 로직, SSE |
| 국현 | frontend-customer | 고객용 주문 웹앱 |
| 수민 | frontend-admin | 관리자용 대시보드 |

## 설계 문서

프로젝트의 전체 설계 문서는 `aidlc-docs/` 디렉토리에 있습니다:

- `inception/requirements/` — 요구사항 정의
- `inception/user-stories/` — 유저 스토리 및 페르소나
- `inception/application-design/` — 애플리케이션 설계, 컴포넌트, API 구조
- `construction/` — 유닛별 기능 설계, NFR, 코드 생성 계획

## 라이선스

Private

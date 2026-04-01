# 테이블오더 서비스 - Unit of Work 정의

---

## 유닛 분해 전략

**아키텍처**: 모놀리식 (단일 백엔드 서버 + 프론트엔드 2개)
**분해 기준**: 배포 단위, 기술 스택, 관심사 분리 기반
**총 유닛 수**: 4개

---

## Unit 1: 데이터베이스 스키마 및 시드 데이터 (Database)

| 항목 | 내용 |
|------|------|
| 이름 | `database` |
| 담당자 | 지현 |
| 기술 스택 | SQLAlchemy 모델 + Alembic 마이그레이션 + MySQL |
| 배포 단위 | DB 마이그레이션 스크립트 |
| 실행 순서 | 1번째 (모든 유닛의 기반) |

**포함 내용**:
- SQLAlchemy ORM 모델 (Store, Table, Menu, Order, User, Session 등)
- Pydantic 스키마 (요청/응답 DTO)
- Alembic 마이그레이션 설정 및 초기 마이그레이션
- 시드 데이터 (매장, 관리자, 샘플 메뉴)
- DB 연결 설정

**책임**:
- 데이터 모델 정의 및 관계 설정
- 스키마 버전 관리
- 초기 데이터 생성

---

## Unit 2: 백엔드 API 서버 (Backend API)

| 항목 | 내용 |
|------|------|
| 이름 | `backend` |
| 담당자 | 소윤 |
| 기술 스택 | Python FastAPI + SQLAlchemy (async) |
| 배포 단위 | 단일 FastAPI 서버 |
| 실행 순서 | 2번째 (Unit 1의 모델/스키마 의존) |

**포함 모듈**:
- BE-AUTH: 인증/인가 (JWT, bcrypt, 역할 권한)
- BE-STORE: 매장 관리
- BE-TABLE: 테이블 관리 및 세션 라이프사이클
- BE-MENU: 메뉴 CRUD 및 카테고리
- BE-ORDER: 주문 CRUD, 상태 관리, 아카이브
- BE-SSE: 실시간 이벤트 스트리밍
- BE-USER: 관리자 계정/역할 관리
- BE-IMAGE: S3 이미지 업로드
- 미들웨어 (Auth, CORS, 보안 헤더, Rate Limiting)

**책임**:
- REST API 엔드포인트 제공
- 비즈니스 로직 처리
- SSE 이벤트 스트리밍
- 인증/인가 처리

---

## Unit 3: 고객용 프론트엔드 (Customer Frontend)

| 항목 | 내용 |
|------|------|
| 이름 | `frontend-customer` |
| 담당자 | 국현 |
| 기술 스택 | Vue.js 3 + Pinia + Vue Router |
| 배포 단위 | 정적 SPA (CDN 또는 웹서버) |
| 실행 순서 | 3번째 (Unit 2 API 의존) |

**포함 기능**:
- 태블릿 자동 로그인 및 세션 관리
- 카테고리별 메뉴 조회 및 상세 보기
- 장바구니 관리 (로컬 저장)
- 주문 생성 및 결과 표시
- 주문 내역 조회
- SSE 기반 주문 상태 실시간 수신

---

## Unit 4: 관리자용 프론트엔드 (Admin Frontend)

| 항목 | 내용 |
|------|------|
| 이름 | `frontend-admin` |
| 담당자 | 수민 |
| 기술 스택 | Vue.js 3 + Pinia + Vue Router |
| 배포 단위 | 정적 SPA (CDN 또는 웹서버) |
| 실행 순서 | 4번째 (Unit 2 API 의존, Unit 3과 병렬 가능) |

**포함 기능**:
- 관리자 로그인 (JWT)
- 실시간 주문 모니터링 대시보드 (SSE)
- 주문 상태 변경 및 삭제
- 테이블 관리 (설정, 이용 완료, 과거 내역)
- 메뉴 CRUD 및 이미지 업로드
- 관리자 계정/역할 관리
- 역할 기반 UI 렌더링 (점주 vs 매니저)

---

## 코드 조직 전략 (Greenfield)

```
table-order/
├── database/                   # Unit 1: DB 스키마 및 시드
│   ├── models/                 # SQLAlchemy ORM 모델
│   ├── schemas/                # Pydantic 스키마
│   ├── seed/                   # 시드 데이터
│   ├── alembic/                # DB 마이그레이션
│   ├── alembic.ini
│   ├── database.py             # DB 연결 설정
│   └── requirements.txt
│
├── backend/                    # Unit 2: FastAPI API 서버
│   ├── app/
│   │   ├── main.py             # FastAPI 앱 엔트리포인트
│   │   ├── config.py           # 설정
│   │   ├── routers/            # API 라우터
│   │   ├── services/           # 비즈니스 로직
│   │   ├── repositories/       # 데이터 접근 계층
│   │   ├── middleware/         # 미들웨어 (auth, cors 등)
│   │   └── utils/              # 유틸리티
│   ├── tests/                  # 단위 테스트
│   └── requirements.txt
│
├── frontend-customer/          # Unit 3: 고객용 Vue.js
│   ├── src/
│   │   ├── views/
│   │   ├── components/
│   │   ├── stores/
│   │   ├── composables/
│   │   ├── services/
│   │   ├── router/
│   │   └── assets/
│   ├── tests/
│   └── package.json
│
├── frontend-admin/             # Unit 4: 관리자용 Vue.js
│   ├── src/
│   │   ├── views/
│   │   ├── components/
│   │   ├── stores/
│   │   ├── composables/
│   │   ├── services/
│   │   ├── router/
│   │   └── assets/
│   ├── tests/
│   └── package.json
│
└── README.md
```

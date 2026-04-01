# Backend Functional Design Plan

## 유닛 정보
- **유닛명**: backend (백엔드 API 서버)
- **기술 스택**: Python FastAPI + SQLAlchemy (async)
- **담당 스토리**: 23개 전체 (US-C01~C08, US-O01~O11, US-M01~M04)
- **포함 모듈**: BE-AUTH, BE-STORE, BE-TABLE, BE-MENU, BE-ORDER, BE-SSE, BE-USER, BE-IMAGE

---

## Functional Design 실행 계획

### Part 1: 질문 수집 및 분석
- [x] Step 1: 유닛 컨텍스트 분석 (unit-of-work.md, story-map.md 참조)
- [x] Step 2: Functional Design 질문 생성 및 파일 저장
- [x] Step 3: 사용자 답변 수집
- [x] Step 4: 답변 분석 및 모순/모호성 검증
- [x] Step 5: (필요 시) 추가 질문 생성 → 불필요

### Part 2: Functional Design 아티팩트 생성
- [x] Step 6: 도메인 엔티티 설계 (domain-entities.md)
  - [x] Store, Table, TableSession 엔티티
  - [x] Menu, Category 엔티티
  - [x] Order, OrderItem, OrderHistory 엔티티
  - [x] User 엔티티
  - [x] 엔티티 간 관계 다이어그램
- [x] Step 7: 비즈니스 로직 모델 설계 (business-logic-model.md)
  - [x] BE-AUTH: 인증/인가 플로우
  - [x] BE-TABLE: 테이블 세션 라이프사이클
  - [x] BE-MENU: 메뉴 CRUD 로직
  - [x] BE-ORDER: 주문 생성/상태 관리/아카이브 로직
  - [x] BE-SSE: 이벤트 브로드캐스트 로직
  - [x] BE-USER: 계정 관리 로직
  - [x] BE-IMAGE: 이미지 업로드 로직
- [x] Step 8: 비즈니스 규칙 정의 (business-rules.md)
  - [x] 인증/인가 규칙 (JWT, 역할 권한, 브루트포스 방지)
  - [x] 주문 상태 전이 규칙
  - [x] 테이블 세션 규칙
  - [x] 데이터 검증 규칙 (메뉴, 주문, 사용자)
  - [x] 역할별 접근 제어 규칙

### Part 3: 승인
- [x] Step 9: 완료 메시지 제시 및 사용자 승인 대기
- [x] Step 10: 승인 기록 및 상태 업데이트

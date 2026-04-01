# 테이블오더 서비스 - 스토리-유닛 매핑

---

## Unit 1: database (DB 스키마 및 시드 데이터)

모든 스토리의 데이터 모델 기반을 제공합니다.

| 스토리 ID | 스토리명 | 관련 모델 |
|-----------|---------|-----------|
| US-C01 | 테이블 태블릿 자동 로그인 | Table, TableSession |
| US-C02~C03 | 메뉴 조회/상세 | Menu, Category |
| US-C06 | 주문 생성 | Order, OrderItem |
| US-C07~C08 | 주문 내역/실시간 | Order, OrderItem |
| US-O01, US-M01 | 관리자/매니저 로그인 | User, Store |
| US-O02~O05 | 주문 모니터링/관리 | Order, OrderItem, OrderHistory |
| US-O06~O08 | 테이블 관리 | Table, TableSession, OrderHistory |
| US-O09~O10 | 메뉴 관리 | Menu, Category |
| US-O11 | 계정 관리 | User |

---

## Unit 2: backend (백엔드 API 서버)

모든 스토리의 API 엔드포인트 및 비즈니스 로직을 담당합니다.

| 스토리 ID | 스토리명 | 관련 모듈 |
|-----------|---------|-----------|
| US-C01 | 테이블 태블릿 자동 로그인 | BE-AUTH, BE-TABLE |
| US-C02 | 카테고리별 메뉴 조회 | BE-MENU |
| US-C03 | 메뉴 상세 정보 확인 | BE-MENU |
| US-C04 | 장바구니에 메뉴 추가 | (클라이언트 전용) |
| US-C05 | 장바구니 수량 조절 및 삭제 | (클라이언트 전용) |
| US-C06 | 주문 생성 | BE-ORDER, BE-SSE |
| US-C07 | 주문 내역 조회 | BE-ORDER |
| US-C08 | 주문 상태 실시간 업데이트 | BE-SSE |
| US-O01 | 관리자 로그인 | BE-AUTH |
| US-O02 | 실시간 주문 모니터링 | BE-ORDER, BE-SSE |
| US-O03 | 주문 상태 변경 | BE-ORDER, BE-SSE |
| US-O04 | 주문 상세 보기 | BE-ORDER |
| US-O05 | 주문 삭제 | BE-ORDER, BE-SSE |
| US-O06 | 테이블 초기 설정 | BE-TABLE |
| US-O07 | 테이블 이용 완료 처리 | BE-TABLE, BE-ORDER |
| US-O08 | 과거 주문 내역 조회 | BE-ORDER |
| US-O09 | 메뉴 등록 | BE-MENU, BE-IMAGE |
| US-O10 | 메뉴 수정 및 삭제 | BE-MENU |
| US-O11 | 관리자 계정 관리 | BE-USER, BE-AUTH |
| US-M01 | 매니저 로그인 | BE-AUTH |
| US-M02 | 실시간 주문 모니터링 (매니저) | BE-ORDER, BE-SSE |
| US-M03 | 테이블 이용 완료 처리 (매니저) | BE-TABLE, BE-ORDER |
| US-M04 | 과거 주문 내역 조회 (매니저) | BE-ORDER |

---

## Unit 3: frontend-customer (고객용 프론트엔드)

| 스토리 ID | 스토리명 | 주요 컴포넌트 |
|-----------|---------|--------------|
| US-C01 | 테이블 태블릿 자동 로그인 | LoginSetup, AutoLogin |
| US-C02 | 카테고리별 메뉴 조회 | MenuList, CategoryTabs |
| US-C03 | 메뉴 상세 정보 확인 | MenuDetail |
| US-C04 | 장바구니에 메뉴 추가 | CartStore, AddToCartButton |
| US-C05 | 장바구니 수량 조절 및 삭제 | CartView, CartItemRow |
| US-C06 | 주문 생성 | OrderConfirm, OrderResult |
| US-C07 | 주문 내역 조회 | OrderHistory, OrderCard |
| US-C08 | 주문 상태 실시간 업데이트 | SSEService, OrderStatusBadge |

---

## Unit 4: frontend-admin (관리자용 프론트엔드)

| 스토리 ID | 스토리명 | 주요 컴포넌트 |
|-----------|---------|--------------|
| US-O01 | 관리자 로그인 | AdminLogin |
| US-O02 | 실시간 주문 모니터링 | Dashboard, TableCard |
| US-O03 | 주문 상태 변경 | OrderStatusButton |
| US-O04 | 주문 상세 보기 | OrderDetailModal |
| US-O05 | 주문 삭제 | OrderDeleteButton, ConfirmDialog |
| US-O06 | 테이블 초기 설정 | TableSetupForm |
| US-O07 | 테이블 이용 완료 처리 | TableCompleteButton, ConfirmDialog |
| US-O08 | 과거 주문 내역 조회 | OrderHistoryModal, DateFilter |
| US-O09 | 메뉴 등록 | MenuForm, ImageUploader |
| US-O10 | 메뉴 수정 및 삭제 | MenuList, MenuForm |
| US-O11 | 관리자 계정 관리 | UserManagement, UserForm |
| US-M01 | 매니저 로그인 | AdminLogin (역할 기반 UI) |
| US-M02 | 실시간 주문 모니터링 (매니저) | Dashboard (제한된 기능) |
| US-M03 | 테이블 이용 완료 처리 (매니저) | TableCompleteButton |
| US-M04 | 과거 주문 내역 조회 (매니저) | OrderHistoryModal |

---

## 커버리지 검증

- **총 스토리**: 23개
- **database 할당**: 23개 (전체 스토리의 데이터 모델 기반)
- **backend 할당**: 23개 (전체 스토리의 API/비즈니스 로직)
- **frontend-customer 할당**: 8개 (US-C01 ~ US-C08)
- **frontend-admin 할당**: 15개 (US-O01 ~ US-O11, US-M01 ~ US-M04)
- **미할당 스토리**: 0개 ✅

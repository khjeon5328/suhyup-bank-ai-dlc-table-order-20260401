# 테이블오더 서비스 - 컴포넌트 메서드 정의

> 상세 비즈니스 로직은 Functional Design(CONSTRUCTION) 단계에서 정의

---

## BE-AUTH: 인증/인가 모듈

| 메서드 | 입력 | 출력 | 목적 |
|--------|------|------|------|
| `login_admin(store_id, username, password)` | str, str, str | JWT TokenPair | 관리자 로그인, JWT 발급 |
| `login_table(store_id, table_no, password)` | str, int, str | JWT Token | 테이블 태블릿 로그인 |
| `verify_token(token)` | str | TokenPayload | JWT 토큰 검증 |
| `check_permission(token, required_role)` | str, Role | bool | 역할 기반 권한 검사 |
| `hash_password(password)` | str | str | bcrypt 해싱 |
| `verify_password(plain, hashed)` | str, str | bool | 비밀번호 검증 |

---

## BE-STORE: 매장 관리 모듈

| 메서드 | 입력 | 출력 | 목적 |
|--------|------|------|------|
| `get_store(store_id)` | int | Store | 매장 정보 조회 |
| `list_stores()` | - | List[Store] | 매장 목록 조회 |

---

## BE-TABLE: 테이블 관리 모듈

| 메서드 | 입력 | 출력 | 목적 |
|--------|------|------|------|
| `setup_table(store_id, table_no, password)` | int, int, str | Table | 테이블 초기 설정 |
| `get_tables(store_id)` | int | List[Table] | 매장 테이블 목록 |
| `get_table(store_id, table_id)` | int, int | Table | 테이블 상세 조회 |
| `start_session(store_id, table_id)` | int, int | Session | 테이블 세션 시작 |
| `end_session(store_id, table_id)` | int, int | Session | 이용 완료 처리 |
| `get_table_summary(store_id)` | int | List[TableSummary] | 테이블별 요약 (총 주문액 등) |

---

## BE-MENU: 메뉴 관리 모듈

| 메서드 | 입력 | 출력 | 목적 |
|--------|------|------|------|
| `create_menu(store_id, menu_data)` | int, MenuCreate | Menu | 메뉴 등록 |
| `get_menus(store_id, category?)` | int, str? | List[Menu] | 메뉴 목록 조회 |
| `get_menu(store_id, menu_id)` | int, int | Menu | 메뉴 상세 조회 |
| `update_menu(store_id, menu_id, menu_data)` | int, int, MenuUpdate | Menu | 메뉴 수정 |
| `delete_menu(store_id, menu_id)` | int, int | bool | 메뉴 삭제 |
| `update_menu_order(store_id, menu_orders)` | int, List[MenuOrder] | bool | 메뉴 노출 순서 변경 |
| `get_categories(store_id)` | int | List[Category] | 카테고리 목록 조회 |

---

## BE-ORDER: 주문 관리 모듈

| 메서드 | 입력 | 출력 | 목적 |
|--------|------|------|------|
| `create_order(store_id, table_id, session_id, items)` | int, int, int, List[OrderItem] | Order | 주문 생성 |
| `get_orders(store_id, table_id?, session_id?)` | int, int?, int? | List[Order] | 주문 목록 조회 |
| `get_order(store_id, order_id)` | int, int | Order | 주문 상세 조회 |
| `update_order_status(store_id, order_id, status)` | int, int, OrderStatus | Order | 주문 상태 변경 |
| `delete_order(store_id, order_id)` | int, int | bool | 주문 삭제 |
| `get_order_history(store_id, table_id, date_from?, date_to?)` | int, int, date?, date? | List[OrderHistory] | 과거 주문 내역 |
| `archive_session_orders(store_id, table_id, session_id)` | int, int, int | bool | 세션 주문 아카이브 |

---

## BE-SSE: 실시간 이벤트 모듈

| 메서드 | 입력 | 출력 | 목적 |
|--------|------|------|------|
| `connect_admin(store_id)` | int | EventStream | 관리자 SSE 연결 |
| `connect_table(store_id, table_id)` | int, int | EventStream | 테이블 SSE 연결 |
| `broadcast_order_event(store_id, event)` | int, OrderEvent | void | 주문 이벤트 브로드캐스트 |
| `disconnect(connection_id)` | str | void | 연결 해제 |

---

## BE-USER: 사용자 관리 모듈

| 메서드 | 입력 | 출력 | 목적 |
|--------|------|------|------|
| `create_user(store_id, user_data)` | int, UserCreate | User | 관리자 계정 생성 |
| `get_users(store_id)` | int | List[User] | 계정 목록 조회 |
| `update_user(store_id, user_id, user_data)` | int, int, UserUpdate | User | 계정 수정 |
| `delete_user(store_id, user_id)` | int, int | bool | 계정 삭제 |

---

## BE-IMAGE: 이미지 업로드 모듈

| 메서드 | 입력 | 출력 | 목적 |
|--------|------|------|------|
| `generate_presigned_url(store_id, filename)` | int, str | PresignedUrl | S3 업로드 URL 생성 |
| `delete_image(image_url)` | str | bool | 이미지 삭제 |

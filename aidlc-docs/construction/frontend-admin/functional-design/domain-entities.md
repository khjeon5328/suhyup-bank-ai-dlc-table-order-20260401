# frontend-admin 도메인 엔티티 정의

> 담당자: 수민 | Unit 4: 관리자용 프론트엔드

---

## 1. 인증 (Auth) 엔티티

### LoginCredentials
```typescript
interface LoginCredentials {
  store_identifier: string;  // 매장 식별자
  username: string;          // 사용자명
  password: string;          // 비밀번호
}
```

### AuthTokens
```typescript
interface AuthTokens {
  access_token: string;      // JWT Access Token (Pinia 메모리 저장)
  token_type: string;        // "bearer"
  // refresh_token은 httpOnly Cookie로 관리 (클라이언트 접근 불가)
}
```

### AuthUser
```typescript
interface AuthUser {
  id: number;
  store_id: number;
  username: string;
  role: UserRole;
  store_name: string;
}
```

### UserRole (Enum)
```typescript
enum UserRole {
  OWNER = 'owner',     // 점주: 전체 기능 접근
  MANAGER = 'manager'  // 매니저: 제한된 기능 접근
}
```

---

## 2. 주문 (Order) 엔티티

### Order
```typescript
interface Order {
  id: number;
  order_number: string;        // 주문 번호 (표시용)
  table_id: number;
  table_number: number;
  session_id: number;
  items: OrderItem[];
  total_amount: number;
  status: OrderStatus;
  created_at: string;          // ISO 8601
  updated_at: string;
}
```

### OrderItem
```typescript
interface OrderItem {
  id: number;
  menu_name: string;
  quantity: number;
  unit_price: number;
  subtotal: number;
}
```

### OrderStatus (Enum)
```typescript
enum OrderStatus {
  PENDING = 'pending',       // 대기중
  PREPARING = 'preparing',   // 준비중
  COMPLETED = 'completed'    // 완료
}
```

### OrderHistory
```typescript
interface OrderHistory {
  id: number;
  order_number: string;
  items: OrderItem[];
  total_amount: number;
  status: OrderStatus;
  created_at: string;
  archived_at: string;        // 이용 완료 시각
}
```

### OrderStatusCount
```typescript
interface OrderStatusCount {
  pending: number;
  preparing: number;
  completed: number;
}
```

---

## 3. 테이블 (Table) 엔티티

### Table
```typescript
interface Table {
  id: number;
  store_id: number;
  table_number: number;
  password: string;            // 테이블 비밀번호 (설정용)
  is_active: boolean;
  current_session_id: number | null;
  created_at: string;
}
```

### TableSession
```typescript
interface TableSession {
  id: number;
  table_id: number;
  table_number: number;
  orders: Order[];
  total_amount: number;
  status_counts: OrderStatusCount;
  started_at: string;
  ended_at: string | null;
}
```

### TableSummary
```typescript
interface TableSummary {
  table_id: number;
  table_number: number;
  has_active_session: boolean;
  total_amount: number;
  order_count: number;
  latest_order: Order | null;
  status_counts: OrderStatusCount;
  has_new_order: boolean;       // NEW 뱃지 표시용
}
```

---

## 4. 메뉴 (Menu) 엔티티

### Menu
```typescript
interface Menu {
  id: number;
  store_id: number;
  category_id: number;
  name: string;
  price: number;
  description: string;
  image_url: string | null;
  display_order: number;
  is_available: boolean;
  created_at: string;
  updated_at: string;
}
```

### MenuCreateRequest
```typescript
interface MenuCreateRequest {
  category_id: number;
  name: string;                // 필수, 1~100자
  price: number;               // 필수, 0 이상
  description?: string;        // 선택, 최대 500자
  image_url?: string;
}
```

### MenuUpdateRequest
```typescript
interface MenuUpdateRequest {
  category_id?: number;
  name?: string;
  price?: number;
  description?: string;
  image_url?: string;
  is_available?: boolean;
}
```

### MenuOrderUpdate
```typescript
interface MenuOrderUpdate {
  id: number;
  display_order: number;
}
```

### Category
```typescript
interface Category {
  id: number;
  store_id: number;
  name: string;
  display_order: number;
  menu_count: number;
  created_at: string;
}
```

### CategoryCreateRequest
```typescript
interface CategoryCreateRequest {
  name: string;                // 필수, 1~50자
}
```

### CategoryUpdateRequest
```typescript
interface CategoryUpdateRequest {
  name?: string;
}
```

### CategoryOrderUpdate
```typescript
interface CategoryOrderUpdate {
  id: number;
  display_order: number;
}
```

---

## 5. 사용자 (User) 엔티티

### User
```typescript
interface User {
  id: number;
  store_id: number;
  username: string;
  role: UserRole;
  created_at: string;
  updated_at: string;
}
```

### UserCreateRequest
```typescript
interface UserCreateRequest {
  username: string;            // 필수, 4~20자, 영문+숫자
  password: string;            // 필수, 8~20자
  role: UserRole;
}
```

### UserUpdateRequest
```typescript
interface UserUpdateRequest {
  password?: string;
  role?: UserRole;
}
```

---

## 6. SSE 이벤트 엔티티

### SSEEvent
```typescript
interface SSEEvent {
  type: SSEEventType;
  data: {
    order_id?: number;
    table_id?: number;
    status?: OrderStatus;
    order?: Order;
  };
  timestamp: string;
}
```

### SSEEventType (Enum)
```typescript
enum SSEEventType {
  ORDER_CREATED = 'order_created',
  ORDER_STATUS_CHANGED = 'order_status_changed',
  ORDER_DELETED = 'order_deleted'
}
```

---

## 7. 공통 (Common) 엔티티

### ApiResponse<T>
```typescript
interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
}
```

### ApiError
```typescript
interface ApiError {
  status: number;
  message: string;
  detail?: string;
  errors?: Record<string, string[]>;
}
```

### PaginatedResponse<T>
```typescript
interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}
```

### DateRange
```typescript
interface DateRange {
  start_date: string;          // YYYY-MM-DD
  end_date: string;            // YYYY-MM-DD
}
```

---

## 엔티티 관계도

```
AuthUser ──── UserRole (owner | manager)
    │
    └── Store
         ├── Table ──── TableSession ──── Order[] ──── OrderItem[]
         ├── Category[] ──── Menu[]
         └── User[]

SSEEvent → Order (실시간 이벤트로 주문 상태 동기화)
```

# E2E Test Instructions - frontend-admin (Cypress)

> 담당자: 수민

---

## 1. 실행 방법

### Cypress 실행 (헤드리스)
```bash
cd frontend-admin
npm run test:e2e
```

### Cypress 실행 (GUI 모드)
```bash
npx cypress open
```

### 사전 요구사항
- frontend-admin 개발 서버 실행 중 (`http://localhost:3001`)
- 백엔드 서버 실행 중 (`http://localhost:8000`)
- 테스트용 데이터 초기화 완료

---

## 2. Cypress 설정

```typescript
// cypress.config.ts
import { defineConfig } from 'cypress'

export default defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3001',
    viewportWidth: 1280,
    viewportHeight: 800,
    defaultCommandTimeout: 10000,
    video: false,
    screenshotOnRunFailure: true,
    specPattern: 'cypress/e2e/**/*.cy.ts',
    supportFile: 'cypress/support/e2e.ts',
  },
})
```

---

## 3. 테스트 시나리오 (4개)

### 시나리오 1: 로그인 플로우 (`login.cy.ts`)

```
describe('로그인')
  ├── it('유효한 자격 증명으로 로그인 성공')
  │   → 매장 식별자, 사용자명, 비밀번호 입력
  │   → 로그인 버튼 클릭
  │   → 대시보드 URL 확인 ('/')
  │   → Sidebar에 사용자명 표시 확인
  │
  ├── it('잘못된 비밀번호로 로그인 실패')
  │   → 잘못된 비밀번호 입력
  │   → 에러 메시지 표시 확인
  │   → 로그인 페이지 유지 확인
  │
  └── it('로그아웃 후 로그인 페이지 이동')
      → 로그인 → 로그아웃 버튼 클릭
      → 로그인 페이지 URL 확인 ('/login')
```

### 시나리오 2: 주문 상태 관리 (`order-status.cy.ts`)

```
describe('주문 상태 관리')
  ├── it('테이블 카드 클릭 시 주문 상세 모달 표시')
  │   → 대시보드에서 테이블 카드 클릭
  │   → OrderDetailModal 표시 확인
  │   → 주문 목록 표시 확인
  │
  ├── it('주문 상태 변경 (pending → preparing)')
  │   → 주문 상세 모달에서 "준비 시작" 버튼 클릭
  │   → 상태 뱃지 "준비중"으로 변경 확인
  │
  └── it('이용 완료 처리')
      → 테이블 카드에서 "이용 완료" 버튼 클릭
      → 확인 팝업에서 "확인" 클릭
      → 테이블 카드 주문 목록 초기화 확인
```

### 시나리오 3: 메뉴 CRUD (`menu-manage.cy.ts`)

```
describe('메뉴 관리')
  ├── it('카테고리 추가')
  │   → 카테고리 이름 입력 → 추가 버튼 클릭
  │   → 카테고리 목록에 추가 확인
  │
  ├── it('메뉴 추가')
  │   → "메뉴 추가" 버튼 클릭
  │   → MenuFormDialog에서 메뉴명, 가격, 설명 입력
  │   → 저장 → 메뉴 목록에 추가 확인
  │
  ├── it('메뉴 수정')
  │   → 메뉴 목록에서 수정 버튼 클릭
  │   → 가격 변경 → 저장
  │   → 변경된 가격 확인
  │
  └── it('메뉴 삭제')
      → 메뉴 목록에서 삭제 버튼 클릭
      → 확인 팝업에서 "확인" 클릭
      → 메뉴 목록에서 제거 확인
```

### 시나리오 4: 역할 기반 접근 제어 (`role-access.cy.ts`)

```
describe('역할 기반 접근 제어')
  ├── it('owner: 전체 메뉴 접근 가능')
  │   → owner 로그인
  │   → Sidebar에 대시보드, 메뉴 관리, 사용자 관리 표시 확인
  │   → /menus 페이지 접근 성공 확인
  │   → /users 페이지 접근 성공 확인
  │
  ├── it('manager: 제한된 메뉴만 표시')
  │   → manager 로그인
  │   → Sidebar에 대시보드만 표시 확인
  │   → 메뉴 관리, 사용자 관리 미표시 확인
  │
  └── it('manager: URL 직접 접근 차단')
      → manager 로그인
      → cy.visit('/menus')
      → 대시보드로 리다이렉트 확인 ('/')
```

---

## 4. 테스트 파일 구조

```
cypress/
├── e2e/
│   ├── login.cy.ts
│   ├── order-status.cy.ts
│   ├── menu-manage.cy.ts
│   └── role-access.cy.ts
├── fixtures/
│   ├── user-owner.json
│   └── user-manager.json
├── support/
│   ├── commands.ts          # 커스텀 커맨드 (cy.login 등)
│   └── e2e.ts               # 글로벌 설정
└── tsconfig.json
```

### 커스텀 커맨드

```typescript
// cypress/support/commands.ts
Cypress.Commands.add('login', (role: 'owner' | 'manager') => {
  const fixture = role === 'owner' ? 'user-owner' : 'user-manager'
  cy.fixture(fixture).then((user) => {
    cy.visit('/login')
    cy.get('[data-cy=store-id]').type(user.storeIdentifier)
    cy.get('[data-cy=username]').type(user.username)
    cy.get('[data-cy=password]').type(user.password)
    cy.get('[data-cy=login-btn]').click()
    cy.url().should('eq', Cypress.config().baseUrl + '/')
  })
})
```

---

## 5. 실행 결과 확인

- 스크린샷: `cypress/screenshots/` (실패 시 자동 저장)
- 리포트: 터미널 출력 (pass/fail 요약)

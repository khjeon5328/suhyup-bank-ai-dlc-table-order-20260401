# Build and Test Summary - frontend-admin

> 담당자: 수민

---

## 빌드 정보

| 항목 | 값 |
|------|-----|
| 빌드 도구 | Vite 5.x |
| 언어 | TypeScript 5.x (strict mode) |
| 프레임워크 | Vue.js 3.4+ |
| UI 라이브러리 | Element Plus 2.x (auto-import) |
| 출력 디렉토리 | `dist/` |
| 예상 초기 로드 | ~235KB (gzip) |
| 개발 서버 포트 | 3001 |

---

## 테스트 요약

| 테스트 유형 | 도구 | 파일 수 | 예상 테스트 수 | 커버리지 목표 |
|------------|------|--------|--------------|-------------|
| 단위 테스트 | Jest 29.x + @vue/test-utils 2.x | 13 | ~33 | 80%+ |
| 통합 테스트 | 수동 (브라우저) | 5 시나리오 | - | - |
| E2E 테스트 | Cypress 13.x | 4 | ~12 | - |

### 단위 테스트 상세

| 카테고리 | 파일 수 | 예상 테스트 수 |
|---------|--------|--------------|
| 서비스 (services) | 4 | ~12 |
| 스토어 (stores) | 5 | ~15 |
| Composable | 2 | ~4 |
| 컴포넌트 | 2 | ~4 |

### 통합 테스트 시나리오

| # | 시나리오 | 검증 항목 |
|---|---------|----------|
| 1 | 인증 플로우 | 로그인 → 토큰 갱신 → 로그아웃 |
| 2 | SSE 모니터링 | 연결 → 이벤트 수신 → UI 반영 |
| 3 | RBAC | owner/manager 역할별 접근 제어 |
| 4 | 메뉴 CRUD | 카테고리/메뉴 생성 → 수정 → 삭제 |
| 5 | 테이블 관리 | 설정 → 주문 처리 → 이용 완료 → 과거 내역 |

### E2E 테스트 시나리오

| # | 시나리오 | 파일 |
|---|---------|------|
| 1 | 로그인 플로우 | `login.cy.ts` |
| 2 | 주문 상태 관리 | `order-status.cy.ts` |
| 3 | 메뉴 CRUD | `menu-manage.cy.ts` |
| 4 | 역할 기반 접근 제어 | `role-access.cy.ts` |

---

## 명령어 참조

| 명령어 | 설명 |
|--------|------|
| `npm install` | 의존성 설치 |
| `npm run dev` | 개발 서버 실행 (포트 3001) |
| `npm run build` | 프로덕션 빌드 |
| `npm run preview` | 빌드 결과 미리보기 |
| `npm test` | 단위 테스트 실행 |
| `npx jest --coverage` | 커버리지 리포트 |
| `npm run test:e2e` | Cypress E2E 테스트 (헤드리스) |
| `npx cypress open` | Cypress GUI 모드 |
| `npm run lint` | ESLint 검사 |
| `npm run format` | Prettier 포맷팅 |

---

## 관련 문서

| 문서 | 경로 |
|------|------|
| 빌드 상세 | `build-and-test/build-instructions.md` |
| 단위 테스트 상세 | `build-and-test/unit-test-instructions.md` |
| 통합 테스트 상세 | `build-and-test/integration-test-instructions.md` |
| E2E 테스트 상세 | `build-and-test/e2e-test-instructions.md` |
| 코드 생성 요약 | `frontend-admin/code/code-generation-summary.md` |
| 기술 스택 | `frontend-admin/nfr-requirements/tech-stack-decisions.md` |
| NFR 디자인 패턴 | `frontend-admin/nfr-design/nfr-design-patterns.md` |
| 논리적 컴포넌트 | `frontend-admin/nfr-design/logical-components.md` |

# Unit 3: frontend-customer - Tech Stack Decisions

> 담당자: 국현

---

## 핵심 기술 스택

| 기술 | 버전 | 용도 | 선택 이유 |
|------|------|------|----------|
| Vue.js | 3.x | UI 프레임워크 | Composition API, 학습 곡선 낮음, 터치 UI 적합 |
| Pinia | 2.x | 상태 관리 | Vue 3 공식 상태 관리, TypeScript 지원 |
| Vue Router | 4.x | 라우팅 | SPA 라우팅, 네비게이션 가드 |
| Vite | 5.x | 빌드 도구 | 빠른 HMR, 최적화된 프로덕션 빌드 |
| Axios | 1.x | HTTP 클라이언트 | 인터셉터, 에러 핸들링 |
| pinia-plugin-persistedstate | 3.x | 상태 영속화 | localStorage 자동 동기화 |

## 개발 도구

| 기술 | 용도 |
|------|------|
| Vitest | 단위 테스트 |
| @vue/test-utils | Vue 컴포넌트 테스트 |
| ESLint + Prettier | 코드 품질/포맷팅 |
| TypeScript | 타입 안전성 (선택적) |

## 의존성 관리
- package-lock.json 커밋 (SECURITY-10)
- 정확한 버전 고정 (^, ~ 미사용)
- npm audit 정기 실행

# Build Instructions - frontend-admin

> 담당자: 수민

---

## 1. 사전 요구사항

- Node.js 18.x 이상
- npm 9.x 이상

## 2. 의존성 설치

```bash
cd frontend-admin
npm install
```

## 3. 환경 변수 설정

`.env.example`을 복사하여 `.env.development` (개발) 또는 `.env.production` (프로덕션) 생성:

```bash
cp .env.example .env.development
```

```env
# .env.development
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_SSE_BASE_URL=http://localhost:8000/api/v1/sse
```

```env
# .env.production
VITE_API_BASE_URL=https://api.example.com/api/v1
VITE_SSE_BASE_URL=https://api.example.com/api/v1/sse
```

## 4. 개발 서버 실행

```bash
npm run dev
```

- 기본 포트: **3001** (`vite.config.ts`에서 설정)
- 접속: `http://localhost:3001`
- HMR 활성화 (코드 변경 시 자동 반영)

## 5. 프로덕션 빌드

```bash
npm run build
```

### 빌드 출력 구조

```
dist/
├── index.html
├── assets/
│   ├── index-[hash].js          # 앱 코드 (~30KB gzip)
│   ├── vendor-vue-[hash].js     # Vue 코어 (~45KB gzip)
│   ├── vendor-element-[hash].js # Element Plus (~120KB gzip)
│   ├── vendor-i18n-[hash].js    # vue-i18n (~15KB gzip)
│   ├── vendor-utils-[hash].js   # axios, dayjs 등 (~25KB gzip)
│   ├── LoginView-[hash].js      # Lazy chunk
│   ├── MenuManageView-[hash].js # Lazy chunk
│   ├── UserManageView-[hash].js # Lazy chunk
│   └── index-[hash].css         # 스타일
```

### 빌드 미리보기

```bash
npm run preview
```

## 6. 린트 및 포맷팅

```bash
# ESLint 검사
npm run lint

# Prettier 포맷팅
npm run format
```

## 7. Troubleshooting

| 문제 | 원인 | 해결 |
|------|------|------|
| `VITE_API_BASE_URL is undefined` | 환경 변수 파일 누락 | `.env.development` 파일 생성 확인 |
| `Module not found` | 의존성 미설치 | `rm -rf node_modules && npm install` |
| `Port 3001 already in use` | 포트 충돌 | 다른 프로세스 종료 또는 `vite.config.ts`에서 포트 변경 |
| Element Plus 스타일 미적용 | auto-import 설정 누락 | `vite.config.ts`에서 ElementPlusResolver 확인 |
| TypeScript 타입 에러 | tsconfig 경로 설정 | `tsconfig.json`의 `paths` 설정 확인 |
| CORS 에러 | 백엔드 CORS 미설정 | 백엔드에서 `http://localhost:3001` 허용 |

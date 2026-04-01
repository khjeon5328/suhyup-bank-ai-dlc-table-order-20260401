# Unit 3: frontend-customer - NFR Design Patterns

> 담당자: 국현

---

## 1. 보안 패턴

### 1.1 HTTP 보안 헤더 (SECURITY-04)
- Vite 프로덕션 빌드 시 `index.html`에 meta 태그로 CSP 설정
- 배포 시 웹서버(Nginx/CloudFront)에서 보안 헤더 추가

### 1.2 입력 검증 패턴 (SECURITY-05)
- 모든 폼 입력에 클라이언트 측 검증 적용
- DOMPurify 또는 Vue의 기본 이스케이프로 XSS 방지
- 서버 측 검증은 백엔드에서 수행 (이중 검증)

### 1.3 토큰 관리 패턴 (SECURITY-08)
```
[Axios 요청 인터셉터]
  → Authorization: Bearer {token} 헤더 자동 추가

[Axios 응답 인터셉터]
  → 401 응답 시 → authStore.logout() → /setup 리다이렉트
```

### 1.4 에러 정보 은닉 (SECURITY-09)
- 프로덕션: 소스맵 비활성화 (`build.sourcemap: false`)
- 프로덕션: Vue devtools 비활성화
- 에러 메시지: 사용자 친화적 메시지만 표시, 내부 정보 미노출

---

## 2. 성능 패턴

### 2.1 이미지 최적화
- `<img loading="lazy">` 적용
- 메뉴 이미지 placeholder 표시 (로딩 중)
- 이미지 로드 실패 시 기본 이미지 표시

### 2.2 컴포넌트 최적화
- 라우트 기반 코드 스플리팅 (`defineAsyncComponent`)
- 메뉴 목록 가상 스크롤 (대량 메뉴 시)
- `v-memo` 디렉티브로 불필요한 리렌더링 방지

### 2.3 API 호출 최적화
- 메뉴 데이터 캐싱 (Pinia 스토어에 저장, 일정 시간 유효)
- 중복 API 호출 방지 (isLoading 플래그)
- 주문 생성 시 버튼 비활성화 (중복 클릭 방지)

---

## 3. 가용성 패턴

### 3.1 SSE 재연결 패턴
```
[SSE 연결]
  → 연결 성공 → 이벤트 수신 대기
  → 연결 끊김 → 3초 대기 → 재연결 시도
  → 재연결 실패 → 재시도 (최대 10회)
  → 10회 초과 → "연결이 끊어졌습니다. 새로고침해 주세요." 표시
```

### 3.2 오프라인 대응
- 장바구니: localStorage에 저장되어 네트워크 무관 유지
- API 실패 시: 에러 메시지 표시 + 재시도 버튼
- 네트워크 복구 시: 자동 SSE 재연결

---

## 4. 에러 핸들링 패턴 (SECURITY-15)

### 4.1 글로벌 에러 핸들러
```
app.config.errorHandler = (err, instance, info) => {
  // 구조화된 로그 기록
  // 사용자에게 안전한 에러 메시지 표시
  // 에러 상태 복구
}
```

### 4.2 API 에러 처리 계층
```
[API 호출]
  → 성공 (2xx) → 정상 처리
  → 클라이언트 에러 (4xx)
    → 401: 인증 만료 → /setup 이동
    → 422: 검증 에러 → 서버 메시지 표시
    → 기타: "요청을 처리할 수 없습니다"
  → 서버 에러 (5xx) → "일시적인 오류가 발생했습니다"
  → 네트워크 에러 → "서버에 연결할 수 없습니다"
```

---

## 5. 로깅 패턴 (SECURITY-03)

### 프로덕션 로깅
```
logger.error({
  timestamp: ISO8601,
  component: 'OrderConfirmView',
  action: 'createOrder',
  message: 'Order creation failed',
  // 토큰, 비밀번호 등 민감 정보 절대 미포함
})
```
- 개발: console.log/error 사용
- 프로덕션: 외부 로깅 서비스 연동 가능 구조

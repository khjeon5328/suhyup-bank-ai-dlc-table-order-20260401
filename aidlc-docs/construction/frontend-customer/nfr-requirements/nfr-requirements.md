# Unit 3: frontend-customer - NFR Requirements

> 담당자: 국현

---

## NFR-FC01: 성능
- 페이지 초기 로드: 3초 이내 (LCP)
- 메뉴 목록 렌더링: 1초 이내
- 장바구니 조작 (추가/삭제/수량변경): 즉시 반응 (< 100ms)
- SSE 이벤트 수신 후 UI 업데이트: 500ms 이내
- 이미지 lazy loading 적용

## NFR-FC02: 보안 (SECURITY-04 준수)
- HTTP 보안 헤더 설정:
  - `Content-Security-Policy`: `default-src 'self'; img-src 'self' https://*.amazonaws.com; connect-src 'self'`
  - `Strict-Transport-Security`: `max-age=31536000; includeSubDomains`
  - `X-Content-Type-Options`: `nosniff`
  - `X-Frame-Options`: `SAMEORIGIN` (태블릿 내장 브라우저 호환)
  - `Referrer-Policy`: `strict-origin-when-cross-origin`

## NFR-FC03: 보안 (SECURITY-05 준수)
- 초기 설정 폼 입력값 검증 (타입, 길이)
- XSS 방지: 사용자 입력 이스케이프
- JWT 토큰은 localStorage에 저장 (httpOnly 쿠키 불가 - SPA)
- 토큰 노출 방지: 로그에 토큰 미포함

## NFR-FC04: 보안 (SECURITY-09 준수)
- 에러 메시지에 내부 정보 미노출 (스택 트레이스, API 경로 등)
- 프로덕션 빌드에서 소스맵 비활성화
- Vue devtools 프로덕션 비활성화

## NFR-FC05: 보안 (SECURITY-10 준수)
- package-lock.json 커밋
- 의존성 정확한 버전 고정
- npm audit 취약점 스캔

## NFR-FC06: 가용성
- SSE 연결 끊김 시 자동 재연결 (3초 간격, 최대 10회)
- 오프라인 시 장바구니 로컬 데이터 유지
- API 실패 시 사용자 친화적 에러 메시지

## NFR-FC07: 사용성
- 터치 친화적 UI (최소 44x44px 터치 영역)
- 반응형 레이아웃 (태블릿 최적화: 768px~1024px)
- 로딩 상태 표시 (스피너/스켈레톤)
- 시각적 피드백 (버튼 탭 시 ripple 효과)

## NFR-FC08: 보안 (SECURITY-15 준수)
- 글로벌 에러 핸들러 설정 (Vue errorHandler)
- 모든 API 호출에 try/catch 적용
- 에러 발생 시 안전한 상태로 복귀 (fail-closed)
- 미처리 Promise rejection 핸들링

## NFR-FC09: 보안 (SECURITY-03 준수)
- 구조화된 로깅 (console.error → 프로덕션에서는 외부 로깅 서비스)
- 민감 정보(토큰, 비밀번호) 로그 미포함
- 에러 로그에 timestamp, 컴포넌트명, 에러 메시지 포함

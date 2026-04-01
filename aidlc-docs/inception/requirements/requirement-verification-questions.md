# 요구사항 검증 질문

아래 질문에 답변해 주세요. 각 질문의 [Answer]: 태그 뒤에 선택한 옵션의 알파벳을 입력해 주세요.
선택지 중 맞는 것이 없으면 마지막 옵션(Other)을 선택하고 설명을 추가해 주세요.

---

## Question 1
백엔드 기술 스택으로 어떤 것을 사용하시겠습니까?

A) Node.js + Express (JavaScript/TypeScript)
B) Spring Boot (Java/Kotlin)
C) Django / FastAPI (Python)
D) NestJS (TypeScript)
X) Other (please describe after [Answer]: tag below)

[Answer]: C

## Question 2
프론트엔드 기술 스택으로 어떤 것을 사용하시겠습니까?

A) React (JavaScript/TypeScript)
B) Vue.js
C) Next.js (React 기반 풀스택)
D) Angular
X) Other (please describe after [Answer]: tag below)

[Answer]: B

## Question 3
데이터베이스로 어떤 것을 사용하시겠습니까?

A) PostgreSQL
B) MySQL
C) MongoDB (NoSQL)
D) SQLite (개발/소규모용)
X) Other (please describe after [Answer]: tag below)

[Answer]: B

## Question 4
배포 환경은 어떻게 계획하고 계십니까?

A) 클라우드 (AWS, Azure, GCP 등)
B) 온프레미스 서버
C) Docker 컨테이너 기반 (배포 환경 미정)
D) 로컬 개발 환경만 우선 구축
X) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 5
매장(Store)은 단일 매장만 지원하면 되나요, 아니면 멀티 매장을 지원해야 하나요?

A) 단일 매장 (하나의 매장만 운영)
B) 멀티 매장 (여러 매장을 하나의 시스템에서 관리)
X) Other (please describe after [Answer]: tag below)

[Answer]: B

## Question 6
관리자 계정은 어떻게 관리하시겠습니까?

A) 매장당 1개의 관리자 계정 (단순)
B) 매장당 여러 관리자 계정 (역할 구분 없음)
C) 매장당 여러 관리자 계정 (역할별 권한 구분: 점주, 매니저 등)
X) Other (please describe after [Answer]: tag below)

[Answer]: C

## Question 7
메뉴 이미지 관리는 어떻게 하시겠습니까?

A) 외부 이미지 URL만 사용 (이미지 업로드 기능 없음)
B) 서버에 직접 이미지 업로드 기능 포함
C) 클라우드 스토리지(S3 등)에 이미지 업로드
X) Other (please describe after [Answer]: tag below)

[Answer]: C

## Question 8
동시 접속 사용자 규모는 어느 정도를 예상하시나요?

A) 소규모 (매장 1~5개, 동시 접속 50명 이하)
B) 중규모 (매장 5~20개, 동시 접속 200명 이하)
C) 대규모 (매장 20개 이상, 동시 접속 500명 이상)
X) Other (please describe after [Answer]: tag below)

[Answer]: C

## Question 9
테이블 태블릿의 세션 만료 시간은 요구사항에 명시되지 않았습니다. 태블릿 자동 로그인 세션의 유효 기간은 어떻게 설정하시겠습니까?

A) 무제한 (한번 설정하면 수동으로 변경할 때까지 유지)
B) 24시간 (매일 자동 갱신)
C) 관리자 세션과 동일하게 16시간
X) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 10
초기 매장 및 관리자 데이터는 어떻게 생성하시겠습니까?

A) 시드 데이터(seed data)로 미리 생성
B) 별도의 슈퍼 관리자 화면에서 매장 등록
C) API를 통한 직접 등록 (관리 UI 없이)
D) 데이터베이스에 직접 입력
X) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 11
주문 상태 실시간 업데이트(고객 화면)는 MVP에 포함하시겠습니까?

A) 포함 (SSE 또는 WebSocket으로 고객 화면에서도 실시간 상태 업데이트)
B) 미포함 (고객은 페이지 새로고침으로 상태 확인)
X) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 12: Security Extensions
이 프로젝트에 보안 확장 규칙(SECURITY rules)을 적용하시겠습니까?

A) Yes — 모든 SECURITY 규칙을 blocking constraint로 적용 (프로덕션 수준 애플리케이션에 권장)
B) No — SECURITY 규칙 건너뛰기 (PoC, 프로토타입, 실험적 프로젝트에 적합)
X) Other (please describe after [Answer]: tag below)

[Answer]: A

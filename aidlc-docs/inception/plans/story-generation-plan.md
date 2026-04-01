# Story Generation Plan - 테이블오더 서비스

## 1. 스토리 개발 질문

아래 질문에 답변해 주세요. 각 질문의 [Answer]: 태그 뒤에 선택한 옵션의 알파벳을 입력해 주세요.

---

### Question 1
스토리 분류(breakdown) 방식은 어떤 것을 선호하시나요?

A) User Journey 기반 - 사용자 워크플로우 흐름에 따라 스토리 구성 (예: 고객 입장 → 메뉴 탐색 → 장바구니 → 주문 → 확인)
B) Feature 기반 - 시스템 기능 단위로 스토리 구성 (예: 인증, 메뉴 관리, 주문 관리 등)
C) Persona 기반 - 사용자 유형별로 스토리 그룹화 (예: 고객 스토리, 점주 스토리, 매니저 스토리)
D) Epic 기반 - 대규모 Epic을 하위 스토리로 분해 (예: Epic: 주문 시스템 → 하위 스토리들)
X) Other (please describe after [Answer]: tag below)

[Answer]: C

### Question 2
스토리의 세분화(granularity) 수준은 어느 정도를 원하시나요?

A) 높은 수준 (High-level) - Epic 수준의 큰 스토리 (예: "고객으로서 메뉴를 주문할 수 있다")
B) 중간 수준 (Medium) - 기능 단위 스토리 (예: "고객으로서 카테고리별 메뉴를 조회할 수 있다")
C) 상세 수준 (Detailed) - 세부 인터랙션 단위 (예: "고객으로서 메뉴 카드를 탭하면 상세 정보를 볼 수 있다")
X) Other (please describe after [Answer]: tag below)

[Answer]: B

### Question 3
수용 기준(Acceptance Criteria) 형식은 어떤 것을 선호하시나요?

A) Given-When-Then (BDD 스타일) - 구조화된 시나리오 형식
B) 체크리스트 형식 - 간단한 검증 항목 목록
C) 혼합 - 복잡한 스토리는 Given-When-Then, 단순한 스토리는 체크리스트
X) Other (please describe after [Answer]: tag below)

[Answer]: C

### Question 4
관리자 역할을 어떻게 구분하시겠습니까?

A) 점주(Owner) + 매니저(Manager) 2단계
B) 점주(Owner) + 매니저(Manager) + 스태프(Staff) 3단계
C) 점주(Owner) + 매니저(Manager) 2단계이며, 매니저는 메뉴 관리/주문 삭제 불가
X) Other (please describe after [Answer]: tag below)

[Answer]: C

### Question 5
스토리 우선순위 표기 방식은 어떤 것을 사용하시겠습니까?

A) MoSCoW (Must/Should/Could/Won't)
B) 높음/중간/낮음 (High/Medium/Low)
C) 숫자 (P1, P2, P3)
X) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## 2. 스토리 생성 실행 계획

아래 체크리스트에 따라 순서대로 실행합니다.

### Phase A: 페르소나 생성
- [x] A1. 고객(Customer) 페르소나 정의
- [x] A2. 점주(Owner) 페르소나 정의
- [x] A3. 매니저(Manager) 페르소나 정의 (Q4 답변에 따라 추가 역할 포함)

### Phase B: 고객용 스토리 생성
- [x] B1. 테이블 태블릿 자동 로그인 및 세션 관리 스토리
- [x] B2. 메뉴 조회 및 탐색 스토리
- [x] B3. 장바구니 관리 스토리
- [x] B4. 주문 생성 스토리
- [x] B5. 주문 내역 조회 스토리

### Phase C: 관리자용 스토리 생성
- [x] C1. 매장 인증 스토리
- [x] C2. 실시간 주문 모니터링 스토리
- [x] C3. 테이블 관리 스토리 (초기 설정, 주문 삭제, 세션 처리, 과거 내역)
- [x] C4. 메뉴 관리 스토리
- [x] C5. 관리자 계정 및 역할 관리 스토리

### Phase D: 검증 및 완성
- [x] D1. INVEST 기준 검증 (Independent, Negotiable, Valuable, Estimable, Small, Testable)
- [x] D2. 페르소나-스토리 매핑 확인
- [x] D3. 수용 기준 완성도 검증
- [x] D4. stories.md 및 personas.md 최종 저장

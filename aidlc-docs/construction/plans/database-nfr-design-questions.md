# NFR Design 질문 - Unit 1: database

database 유닛의 NFR 설계 패턴을 확정하기 위해 아래 질문에 답변해 주세요.
각 질문의 `[Answer]:` 태그 뒤에 선택지 알파벳을 입력해 주세요.

---

## Question 1
데이터 접근 패턴을 어떻게 설계할까요?

A) Repository 패턴 — 엔티티별 Repository 클래스를 만들어 CRUD 로직 캡슐화 (backend 유닛에서 Repository를 통해 DB 접근)
B) 직접 세션 사용 — backend 유닛의 Service 레이어에서 SQLAlchemy 세션을 직접 사용 (별도 Repository 없음)
C) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 2
SQLAlchemy 모델의 공통 필드(created_at, updated_at) 처리 방식을 어떻게 할까요?

A) Mixin 클래스 — TimestampMixin을 만들어 모든 모델에 상속 적용
B) Base 모델 확장 — DeclarativeBase를 확장한 커스텀 Base에 공통 필드 포함
C) 개별 정의 — 각 모델에 직접 created_at, updated_at 필드 정의
D) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 3
소프트 삭제 구현 패턴을 어떻게 할까요?

A) Mixin + 쿼리 필터 — SoftDeleteMixin 클래스 + 기본 쿼리에 deleted_at IS NULL 자동 필터 적용
B) Mixin만 — SoftDeleteMixin으로 deleted_at 필드만 제공, 필터는 서비스 레이어에서 수동 적용
C) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 4
환경별 설정(DB 접속 정보, TLS 등) 관리 패턴을 어떻게 할까요?

A) Pydantic Settings — pydantic-settings의 BaseSettings로 환경 변수 자동 로드 + 타입 검증
B) python-dotenv 직접 — dotenv로 .env 로드 후 os.environ으로 접근
C) 설정 딕셔너리 — config.py에 환경별 딕셔너리 정의
D) Other (please describe after [Answer]: tag below)

[Answer]: A


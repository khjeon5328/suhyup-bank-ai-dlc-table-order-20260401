# 테이블오더 서비스 - Unit of Work 의존성

---

## 의존성 매트릭스

| 유닛 | 의존 대상 | 통신 방식 | 의존 유형 |
|------|----------|-----------|-----------|
| database | MySQL | DB 프로토콜 | 인프라 의존 |
| backend | database, S3 | Python import, HTTPS | 모듈 의존, 인프라 의존 |
| frontend-customer | backend | HTTPS REST, SSE | API 의존 |
| frontend-admin | backend | HTTPS REST, SSE | API 의존 |

---

## 의존성 다이어그램

```
+--------------------+     +--------------------+
| frontend-customer  |     | frontend-admin     |
| (Vue.js SPA)       |     | (Vue.js SPA)       |
+--------+-----------+     +-----------+--------+
         |                              |
         |    HTTPS REST + SSE          |
         +-------------+---------------+
                       |
               +-------v--------+
               |    backend     |
               |   (FastAPI)    |
               +-------+--------+
                       |
               +-------v--------+
               |   database     |
               | (Models/Schema)|
               +---+--------+--+
                   |        |
            +------v-+  +--v------+
            | MySQL  |  |   S3    |
            +--------+  +---------+
```

---

## 개발 순서

| 순서 | 유닛 | 이유 |
|------|------|------|
| 1 | database | 모든 유닛의 기반. 모델, 스키마, 시드 데이터가 먼저 정의되어야 함 |
| 2 | backend | database의 모델/스키마를 import하여 API 구현. 프론트엔드의 의존 대상 |
| 3 | frontend-customer | 고객 주문이 핵심 플로우. 백엔드 API 완성 후 연동 |
| 4 | frontend-admin | 관리 기능. Unit 3과 병렬 개발 가능 |

**참고**: Unit 3과 Unit 4는 서로 의존성이 없으므로 병렬 개발 가능

---

## 유닛 간 인터페이스

### database → backend
- Python import: SQLAlchemy 모델, Pydantic 스키마, DB 연결 설정
- backend가 database 패키지의 모델/스키마를 직접 참조

### backend → frontend-customer
- REST API: 메뉴 조회, 주문 생성/조회, 테이블 로그인
- SSE: 주문 상태 변경 이벤트

### backend → frontend-admin
- REST API: 전체 관리 API (메뉴, 주문, 테이블, 사용자, 이미지)
- SSE: 신규 주문, 주문 상태 변경, 주문 삭제 이벤트

### backend → S3
- Presigned URL 생성 (boto3)
- 프론트엔드가 직접 S3에 업로드

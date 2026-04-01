# 테이블오더 Backend API

FastAPI 기반 테이블오더 서비스 백엔드 API 서버

## 기술 스택
- Python 3.11+ / FastAPI / SQLAlchemy 2.0 (async) / MySQL
- JWT 인증 / bcrypt / structlog / SSE

## 설치 및 실행

```bash
# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일 수정

# 서버 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 테스트 실행

```bash
pytest --cov=app tests/ -v
```

## API 문서
서버 실행 후 접속:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 프로젝트 구조
```
backend/
  app/
    main.py          # FastAPI 앱 엔트리포인트
    config.py        # Pydantic Settings
    core/            # Cross-cutting (DB, 보안, 이벤트, DI)
    middleware/      # 보안 헤더, Request ID
    models/          # SQLAlchemy ORM 모델
    schemas/         # Pydantic 스키마
    repositories/    # 데이터 접근 레이어
    services/        # 비즈니스 로직 레이어
    routers/         # API 라우터 레이어
  tests/             # 단위 테스트
```

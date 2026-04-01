# Backend Code Generation Summary

## 생성된 파일 목록

### 설정 (3개)
- `backend/requirements.txt`
- `backend/.env.example`
- `backend/app/config.py`

### Core (7개)
- `backend/app/main.py`
- `backend/app/core/database.py`
- `backend/app/core/exceptions.py`
- `backend/app/core/security.py`
- `backend/app/core/event_bus.py`
- `backend/app/core/sse_manager.py`
- `backend/app/core/dependencies.py`
- `backend/app/core/logging_config.py`

### Middleware (2개)
- `backend/app/middleware/security_headers.py`
- `backend/app/middleware/request_id.py`

### Models (11개)
- `backend/app/models/store.py` ~ `login_attempt.py`

### Schemas (8개)
- `backend/app/schemas/common.py` ~ `image.py`

### Repositories (10개)
- `backend/app/repositories/store_repo.py` ~ `login_attempt_repo.py`

### Services (7개)
- `backend/app/services/auth_service.py` ~ `image_service.py`

### Routers (8개)
- `backend/app/routers/auth.py` ~ `events.py`

### Tests (14개)
- `backend/tests/conftest.py`
- `backend/tests/test_core/` (3개)
- `backend/tests/test_services/` (5개)
- `backend/tests/test_routers/` (5개)

### Documentation (1개)
- `backend/README.md`

## 스토리 커버리지: 21/23 (US-C04, US-C05는 클라이언트 전용)

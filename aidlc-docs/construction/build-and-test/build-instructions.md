# Build Instructions - 테이블오더 서비스

## Prerequisites
- Python 3.11+
- Node.js 18+
- MySQL 8.0+
- npm 9+

## Environment Variables

### database (Unit 1)
```bash
cp table-order/database/.env.example table-order/database/.env
# DATABASE_URL=mysql+aiomysql://user:password@localhost:3306/table_order
```

### backend (Unit 2)
```bash
cp backend/.env.example backend/.env
# DATABASE_URL, JWT_SECRET_KEY, CORS_ORIGINS, S3 설정 등
```

### frontend-customer (Unit 3)
```bash
cp frontend-customer/.env.example frontend-customer/.env
# VITE_API_BASE_URL=/api/v1
```

### frontend-admin (Unit 4)
```bash
cp frontend-admin/.env.example frontend-admin/.env
# VITE_API_BASE_URL=/api/v1
```

---

## Build Steps

### 1. MySQL 데이터베이스 생성
```bash
mysql -u root -p -e "CREATE DATABASE table_order CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

### 2. Unit 1: database — 마이그레이션 및 시드
```bash
cd table-order/database
pip install -r requirements.txt
alembic upgrade head
python -m seed.run_seed
```

### 3. Unit 2: backend — 의존성 설치 및 서버 실행
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Unit 3: frontend-customer — 빌드
```bash
cd frontend-customer
npm install
npm run build    # 프로덕션 빌드 → dist/
npm run dev      # 개발 서버 → http://localhost:3000
```

### 5. Unit 4: frontend-admin — 빌드
```bash
cd frontend-admin
npm install
npm run build    # 프로덕션 빌드 → dist/
npm run dev      # 개발 서버 → http://localhost:3001
```

---

## Verify Build Success
- backend: `http://localhost:8000/health` → `{"status": "ok"}`
- frontend-customer: `http://localhost:3000` → 테이블 설정 화면
- frontend-admin: `http://localhost:3001` → 관리자 로그인 화면

## 시드 데이터 기본 계정
- 매장 코드: `STORE001`
- 점주: username `owner`, password (시드에서 설정)
- 매니저: username `manager`, password (시드에서 설정)
- 테이블: 1~5번

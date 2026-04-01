# Unit Test Execution - 테이블오더 서비스

## Unit 1: database
```bash
cd table-order/database
pip install -r requirements.txt
pytest tests/ -v
```
**예상 테스트**: 모델 테스트, 리포지토리 테스트, 스키마 테스트, 보안 테스트

## Unit 2: backend
```bash
cd backend
pip install -r requirements.txt
pytest tests/ -v --tb=short
```
**예상 테스트**: 서비스 테스트 (auth, menu, order, table, user), 라우터 테스트, 코어 테스트 (event_bus, exceptions, security)

## Unit 3: frontend-customer
```bash
cd frontend-customer
npm install
npm run test
```
**예상 테스트**: cartStore, authStore, formatters, validators

## Unit 4: frontend-admin
```bash
cd frontend-admin
npm install
npm run test
```
**예상 테스트**: (수민 유닛 완료 후 확인)

---

## 전체 테스트 한번에 실행
```bash
# database
cd table-order/database && pytest tests/ -v && cd ../..

# backend
cd backend && pytest tests/ -v && cd ..

# frontend-customer
cd frontend-customer && npm run test && cd ..

# frontend-admin
cd frontend-admin && npm run test && cd ..
```

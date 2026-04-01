# Integration Test Instructions - 테이블오더 서비스

## 목적
유닛 간 연동이 정상 동작하는지 검증합니다.

---

## 사전 준비
```bash
# 1. MySQL 실행 및 DB 생성
# 2. 마이그레이션 + 시드 실행
cd table-order/database && alembic upgrade head && python -m seed.run_seed && cd ../..

# 3. 백엔드 서버 실행
cd backend && uvicorn app.main:app --port 8000 &

# 4. 프론트엔드 개발 서버 실행
cd frontend-customer && npm run dev &
cd frontend-admin && npm run dev &
```

---

## 통합 테스트 시나리오

### Scenario 1: 테이블 로그인 (Unit 3 → Unit 2 → Unit 1)
1. frontend-customer에서 매장 코드 `STORE001`, 테이블 번호 `1`, 비밀번호 입력
2. **검증**: 로그인 성공, 메뉴 화면 표시, JWT 토큰 localStorage 저장

### Scenario 2: 메뉴 조회 (Unit 3 → Unit 2 → Unit 1)
1. 로그인 후 메뉴 화면에서 카테고리 탭 확인
2. **검증**: 시드 데이터의 3개 카테고리, 10개 메뉴가 표시됨

### Scenario 3: 주문 생성 → 실시간 모니터링 (Unit 3 → Unit 2 → Unit 4)
1. frontend-customer에서 메뉴 2개를 장바구니에 추가
2. 주문 확정
3. frontend-admin 대시보드에서 신규 주문 확인
4. **검증**: 주문 번호 표시, 5초 후 리다이렉트, 관리자 대시보드에 SSE로 실시간 표시

### Scenario 4: 주문 상태 변경 → 고객 실시간 업데이트 (Unit 4 → Unit 2 → Unit 3)
1. frontend-admin에서 주문 상태를 "대기중" → "준비중" 변경
2. frontend-customer 주문 내역에서 상태 확인
3. **검증**: SSE를 통해 고객 화면에 "준비중" 실시간 반영

### Scenario 5: 테이블 이용 완료 (Unit 4 → Unit 2 → Unit 1)
1. frontend-admin에서 테이블 "이용 완료" 처리
2. **검증**: 주문이 과거 이력으로 이동, 테이블 총 주문액 0 리셋, 고객 화면 장바구니 비워짐

### Scenario 6: 역할 기반 접근 제어 (Unit 4 → Unit 2)
1. 매니저 계정으로 로그인
2. **검증**: 메뉴 관리, 주문 삭제, 계정 관리 메뉴 미표시/접근 불가

### Scenario 7: 관리자 로그인 브루트포스 방지 (Unit 4 → Unit 2)
1. 잘못된 비밀번호로 5회 연속 로그인 시도
2. **검증**: 계정 잠금 메시지 표시

---

## 정리
```bash
# 서버 종료
kill %1 %2 %3  # 백그라운드 프로세스 종료
```

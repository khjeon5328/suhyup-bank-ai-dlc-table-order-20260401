# Unit 4: frontend-admin - 프론트엔드 컴포넌트 설계

> 담당자: 수민

## 페이지 구조
```
App.vue
├── LoginView.vue                    # 관리자 로그인
├── DashboardView.vue                # 실시간 주문 모니터링 (기본)
│   ├── TableCard.vue
│   │   └── OrderStatusBadge.vue
│   ├── OrderDetailModal.vue
│   └── OrderHistoryModal.vue
├── MenuManageView.vue               # 메뉴 관리 (점주만)
│   ├── MenuForm.vue
│   └── ImageUploader.vue
├── TableManageView.vue              # 테이블 관리
│   └── TableSetupForm.vue
└── UserManageView.vue               # 계정 관리 (점주만)
    └── UserForm.vue
```

## 라우터: /login, / (대시보드), /menus (점주), /tables, /users (점주)
## Pinia 스토어: authStore, orderStore, menuStore, tableStore, userStore
## 역할 분기: 점주=전체, 매니저=대시보드+테이블이용완료+과거내역만

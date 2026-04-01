"""Seed data definitions for development/test environments."""

STORES = [
    {"store_code": "PIZZA01", "name": "마리오 피자", "address": "서울시 강남구 테헤란로 123", "phone": "02-1234-5678"},
    {"store_code": "CHICKEN01", "name": "황금 치킨", "address": "서울시 서초구 서초대로 456", "phone": "02-9876-5432"},
]

USERS = [
    # PIZZA01
    {"store_code": "PIZZA01", "username": "admin", "password": "password123", "role": "owner"},
    {"store_code": "PIZZA01", "username": "manager1", "password": "password123", "role": "manager"},
    # CHICKEN01
    {"store_code": "CHICKEN01", "username": "admin", "password": "password123", "role": "owner"},
    {"store_code": "CHICKEN01", "username": "manager1", "password": "password123", "role": "manager"},
]

TABLES = [
    # PIZZA01: tables 1-5
    *[{"store_code": "PIZZA01", "table_no": i, "password": "1234"} for i in range(1, 6)],
    # CHICKEN01: tables 1-5
    *[{"store_code": "CHICKEN01", "table_no": i, "password": "1234"} for i in range(1, 6)],
]

CATEGORIES = [
    # PIZZA01
    {"store_code": "PIZZA01", "name": "피자", "sort_order": 1},
    {"store_code": "PIZZA01", "name": "파스타", "sort_order": 2},
    {"store_code": "PIZZA01", "name": "음료", "sort_order": 3},
    {"store_code": "PIZZA01", "name": "디저트", "sort_order": 4},
    # CHICKEN01
    {"store_code": "CHICKEN01", "name": "치킨", "sort_order": 1},
    {"store_code": "CHICKEN01", "name": "사이드", "sort_order": 2},
    {"store_code": "CHICKEN01", "name": "음료", "sort_order": 3},
    {"store_code": "CHICKEN01", "name": "세트메뉴", "sort_order": 4},
]

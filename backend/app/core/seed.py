"""Seed data for development — creates sample store, admin, tables, categories, menus."""

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.category import Category
from app.models.menu import Menu
from app.models.store import Store
from app.models.table import RestaurantTable
from app.models.table_session import TableSession
from app.models.user import User, UserRole

logger = structlog.get_logger()


async def seed_data(session: AsyncSession) -> None:
    """Insert seed data if store doesn't exist yet."""
    result = await session.execute(select(Store).where(Store.store_code == "STORE01"))
    if result.scalar_one_or_none():
        logger.info("seed_skipped", reason="data already exists")
        return

    # Store
    store = Store(store_code="STORE01", name="맛있는 식당", address="서울시 강남구", phone="02-1234-5678")
    session.add(store)
    await session.flush()

    # Admin users
    owner = User(store_code="STORE01", username="admin", password_hash=hash_password("admin1234"), role=UserRole.OWNER)
    manager = User(store_code="STORE01", username="manager", password_hash=hash_password("manager1234"), role=UserRole.MANAGER)
    session.add_all([owner, manager])

    # Tables (1~5)
    for i in range(1, 6):
        table = RestaurantTable(store_code="STORE01", table_no=i, password_hash=hash_password("1234"))
        session.add(table)
        await session.flush()
        ts = TableSession(store_code="STORE01", table_no=i)
        session.add(ts)

    # Categories
    categories = ["메인", "사이드", "음료"]
    cat_objs = []
    for idx, name in enumerate(categories):
        cat = Category(store_code="STORE01", name=name, sort_order=idx + 1)
        session.add(cat)
        await session.flush()
        cat_objs.append(cat)

    # Menus
    menus = [
        ("김치찌개", 9000, "메인", "얼큰한 김치찌개"),
        ("된장찌개", 8000, "메인", "구수한 된장찌개"),
        ("제육볶음", 11000, "메인", "매콤한 제육볶음"),
        ("비빔밥", 9500, "메인", "건강한 비빔밥"),
        ("계란말이", 5000, "사이드", "부드러운 계란말이"),
        ("김치전", 6000, "사이드", "바삭한 김치전"),
        ("콜라", 2000, "음료", "시원한 콜라"),
        ("사이다", 2000, "음료", "청량한 사이다"),
        ("맥주", 5000, "음료", "시원한 생맥주"),
    ]
    cat_map = {c.name: c.id for c in cat_objs}
    for idx, (name, price, cat_name, desc) in enumerate(menus):
        menu = Menu(
            store_code="STORE01", category_id=cat_map[cat_name],
            name=name, price=price, description=desc, sort_order=idx + 1,
        )
        session.add(menu)

    await session.commit()
    logger.info("seed_completed", store_code="STORE01", menus=len(menus), tables=5)

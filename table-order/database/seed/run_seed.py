"""Seed execution script. Idempotent - skips if data already exists."""

import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import async_session_factory, engine
from ..models import Base, Category, Menu, RestaurantTable, Store, User
from ..utils.security import hash_password
from .menus import MENUS
from .seed_data import CATEGORIES, STORES, TABLES, USERS


async def seed_stores(session: AsyncSession) -> None:
    """Seed store data."""
    for data in STORES:
        existing = await session.get(Store, data["store_code"])
        if not existing:
            session.add(Store(**data))


async def seed_users(session: AsyncSession) -> None:
    """Seed user data with hashed passwords."""
    for data in USERS:
        stmt = select(User).where(
            User.store_code == data["store_code"],
            User.username == data["username"],
        )
        result = await session.execute(stmt)
        if not result.scalar_one_or_none():
            session.add(User(
                store_code=data["store_code"],
                username=data["username"],
                password_hash=hash_password(data["password"]),
                role=data["role"],
            ))


async def seed_tables(session: AsyncSession) -> None:
    """Seed table data with hashed PINs."""
    for data in TABLES:
        existing = await session.get(
            RestaurantTable, (data["store_code"], data["table_no"])
        )
        if not existing:
            session.add(RestaurantTable(
                store_code=data["store_code"],
                table_no=data["table_no"],
                password_hash=hash_password(data["password"]),
            ))


async def seed_categories(session: AsyncSession) -> None:
    """Seed category data."""
    for data in CATEGORIES:
        stmt = select(Category).where(
            Category.store_code == data["store_code"],
            Category.name == data["name"],
        )
        result = await session.execute(stmt)
        if not result.scalar_one_or_none():
            session.add(Category(**data))


async def seed_menus(session: AsyncSession) -> None:
    """Seed menu data. Requires categories to exist."""
    for data in MENUS:
        category_stmt = select(Category).where(
            Category.store_code == data["store_code"],
            Category.name == data["category_name"],
        )
        result = await session.execute(category_stmt)
        category = result.scalar_one_or_none()
        if not category:
            continue

        menu_stmt = select(Menu).where(
            Menu.store_code == data["store_code"],
            Menu.name == data["name"],
            Menu.deleted_at.is_(None),
        )
        result = await session.execute(menu_stmt)
        if not result.scalar_one_or_none():
            session.add(Menu(
                store_code=data["store_code"],
                category_id=category.id,
                name=data["name"],
                price=data["price"],
                description=data.get("description"),
                sort_order=data.get("sort_order", 0),
            ))


async def run_seed() -> None:
    """Execute all seed functions in order. Idempotent."""
    async with async_session_factory() as session:
        try:
            await seed_stores(session)
            await session.flush()

            await seed_users(session)
            await seed_tables(session)
            await seed_categories(session)
            await session.flush()

            await seed_menus(session)
            await session.commit()
            print("Seed data loaded successfully.")
        except Exception as e:
            await session.rollback()
            print(f"Seed failed: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(run_seed())

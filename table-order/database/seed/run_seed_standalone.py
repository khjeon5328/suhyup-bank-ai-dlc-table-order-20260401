"""Standalone seed runner for Docker — no relative imports."""
import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import async_session_factory, engine
from models import Base, Category, Menu, RestaurantTable, Store, User
from utils.security import hash_password
from seed.menus import MENUS
from seed.seed_data import CATEGORIES, STORES, TABLES, USERS
from sqlalchemy import select


async def run():
    async with async_session_factory() as session:
        try:
            for data in STORES:
                existing = await session.get(Store, data["store_code"])
                if not existing:
                    session.add(Store(**data))
            await session.flush()

            for data in USERS:
                stmt = select(User).where(User.store_code == data["store_code"], User.username == data["username"])
                result = await session.execute(stmt)
                if not result.scalar_one_or_none():
                    session.add(User(store_code=data["store_code"], username=data["username"], password_hash=hash_password(data["password"]), role=data["role"]))

            for data in TABLES:
                existing = await session.get(RestaurantTable, (data["store_code"], data["table_no"]))
                if not existing:
                    session.add(RestaurantTable(store_code=data["store_code"], table_no=data["table_no"], password_hash=hash_password(data["password"])))

            for data in CATEGORIES:
                stmt = select(Category).where(Category.store_code == data["store_code"], Category.name == data["name"])
                result = await session.execute(stmt)
                if not result.scalar_one_or_none():
                    session.add(Category(**data))
            await session.flush()

            for data in MENUS:
                cat_stmt = select(Category).where(Category.store_code == data["store_code"], Category.name == data["category_name"])
                result = await session.execute(cat_stmt)
                category = result.scalar_one_or_none()
                if not category:
                    continue
                menu_stmt = select(Menu).where(Menu.store_code == data["store_code"], Menu.name == data["name"], Menu.deleted_at.is_(None))
                result = await session.execute(menu_stmt)
                if not result.scalar_one_or_none():
                    session.add(Menu(store_code=data["store_code"], category_id=category.id, name=data["name"], price=data["price"], description=data.get("description"), sort_order=data.get("sort_order", 0)))

            await session.commit()
            print("Seed data loaded successfully.")
        except Exception as e:
            await session.rollback()
            print(f"Seed failed: {e}")
            raise

if __name__ == "__main__":
    asyncio.run(run())

"""Category repository."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.category import Category
from .base import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    """Repository for Category entity."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Category)

    async def get_by_store(
        self, store_code: str, ordered: bool = True
    ) -> list[Category]:
        """Get all categories for a store."""
        stmt = select(Category).where(Category.store_code == store_code)
        if ordered:
            stmt = stmt.order_by(Category.sort_order, Category.id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_name(
        self, store_code: str, name: str
    ) -> Category | None:
        """Get category by store and name."""
        stmt = select(Category).where(
            Category.store_code == store_code,
            Category.name == name,
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

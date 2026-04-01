"""Base repository with generic CRUD operations."""

from typing import Any, Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.base import Base

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    """Generic base repository providing common CRUD operations."""

    def __init__(self, session: AsyncSession, model: type[T]) -> None:
        self.session = session
        self.model = model

    async def get_by_id(self, id_value: Any) -> T | None:
        """Get a single record by primary key."""
        return await self.session.get(self.model, id_value)

    async def get_all(
        self,
        filters: list | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[T]:
        """Get all records with optional filters and pagination."""
        stmt = select(self.model)
        if filters:
            for f in filters:
                stmt = stmt.where(f)
        stmt = stmt.offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def count(self, filters: list | None = None) -> int:
        """Count records with optional filters."""
        from sqlalchemy import func

        stmt = select(func.count()).select_from(self.model)
        if filters:
            for f in filters:
                stmt = stmt.where(f)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def create(self, entity: T) -> T:
        """Create a new record."""
        self.session.add(entity)
        await self.session.flush()
        await self.session.refresh(entity)
        return entity

    async def delete(self, entity: T) -> bool:
        """Hard delete a record."""
        await self.session.delete(entity)
        await self.session.flush()
        return True

"""Order repository with archive support."""

from datetime import date, datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.order import Order
from .base import BaseRepository


class OrderRepository(BaseRepository[Order]):
    """Repository for Order entity with archive support."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Order)

    async def get_current_orders(
        self, store_code: str, table_no: int | None = None
    ) -> list[Order]:
        """Get current (non-archived) orders for a store."""
        stmt = select(Order).where(
            Order.store_code == store_code,
            Order.archived_at.is_(None),
        )
        if table_no is not None:
            stmt = stmt.where(Order.table_no == table_no)
        stmt = stmt.order_by(Order.created_at.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_session_orders(self, session_id: int) -> list[Order]:
        """Get all orders for a specific session."""
        stmt = (
            select(Order)
            .where(Order.session_id == session_id, Order.archived_at.is_(None))
            .order_by(Order.created_at.desc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_archived_orders(
        self,
        store_code: str,
        table_no: int | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> list[Order]:
        """Get archived (past) orders with optional filters."""
        stmt = select(Order).where(
            Order.store_code == store_code,
            Order.archived_at.is_not(None),
        )
        if table_no is not None:
            stmt = stmt.where(Order.table_no == table_no)
        if date_from is not None:
            stmt = stmt.where(Order.created_at >= datetime.combine(date_from, datetime.min.time()))
        if date_to is not None:
            stmt = stmt.where(
                Order.created_at < datetime.combine(date_to, datetime.max.time())
            )
        stmt = stmt.order_by(Order.created_at.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def archive_by_session(self, session_id: int) -> int:
        """Archive all orders for a session. Returns count of archived orders."""
        orders = await self.get_session_orders(session_id)
        now = datetime.now(timezone.utc)
        count = 0
        for order in orders:
            order.archived_at = now
            count += 1
        await self.session.flush()
        return count

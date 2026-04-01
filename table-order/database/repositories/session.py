"""TableSession repository."""

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.session import TableSession
from .base import BaseRepository


class SessionRepository(BaseRepository[TableSession]):
    """Repository for TableSession entity."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, TableSession)

    async def get_active_session(
        self, store_code: str, table_no: int
    ) -> TableSession | None:
        """Get the active session for a table (ended_at IS NULL)."""
        stmt = select(TableSession).where(
            TableSession.store_code == store_code,
            TableSession.table_no == table_no,
            TableSession.ended_at.is_(None),
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_session(
        self, store_code: str, table_no: int
    ) -> TableSession:
        """Create a new active session for a table."""
        new_session = TableSession(
            store_code=store_code,
            table_no=table_no,
        )
        return await self.create(new_session)

    async def end_session(self, session_id: int) -> TableSession | None:
        """End a session by setting ended_at."""
        table_session = await self.get_by_id(session_id)
        if table_session and table_session.is_active:
            table_session.ended_at = datetime.now(timezone.utc)
            await self.session.flush()
            await self.session.refresh(table_session)
            return table_session
        return None

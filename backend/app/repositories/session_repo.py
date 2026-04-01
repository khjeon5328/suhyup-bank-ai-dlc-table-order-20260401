"""TableSession repository."""

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.table_session import TableSession


class SessionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, session: TableSession) -> TableSession:
        self.db.add(session)
        await self.db.flush()
        await self.db.refresh(session)
        return session

    async def get_active(self, table_id: int) -> Optional[TableSession]:
        result = await self.db.execute(
            select(TableSession).where(TableSession.table_id == table_id, TableSession.is_active == True)
        )
        return result.scalar_one_or_none()

    async def deactivate(self, session: TableSession) -> TableSession:
        session.is_active = False
        session.ended_at = datetime.now(timezone.utc)
        await self.db.flush()
        return session

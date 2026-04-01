"""TableSession repository — synced with Unit 1."""

from datetime import datetime
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

    async def get_active(self, store_code: str, table_no: int) -> Optional[TableSession]:
        result = await self.db.execute(
            select(TableSession).where(
                TableSession.store_code == store_code,
                TableSession.table_no == table_no,
                TableSession.ended_at.is_(None),
            )
        )
        return result.scalar_one_or_none()

    async def deactivate(self, session: TableSession) -> TableSession:
        session.ended_at = datetime.utcnow()
        await self.db.flush()
        return session

"""LoginAttempt repository for brute-force protection."""

from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.login_attempt import LoginAttempt


class LoginAttemptRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, attempt: LoginAttempt) -> LoginAttempt:
        self.db.add(attempt)
        await self.db.flush()
        return attempt

    async def count_recent_by_ip(self, ip_address: str, minutes: int = 15) -> int:
        since = datetime.now(timezone.utc) - timedelta(minutes=minutes)
        result = await self.db.execute(
            select(func.count()).where(
                LoginAttempt.ip_address == ip_address,
                LoginAttempt.success == False,
                LoginAttempt.attempted_at >= since,
            )
        )
        return result.scalar_one()

    async def count_recent_by_account(
        self, store_id: int, username: str, minutes: int = 15
    ) -> int:
        since = datetime.now(timezone.utc) - timedelta(minutes=minutes)
        result = await self.db.execute(
            select(func.count()).where(
                LoginAttempt.store_id == store_id,
                LoginAttempt.username == username,
                LoginAttempt.success == False,
                LoginAttempt.attempted_at >= since,
            )
        )
        return result.scalar_one()

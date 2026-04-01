"""TableSession schemas."""

from datetime import datetime

from pydantic import BaseModel


class SessionResponse(BaseModel):
    """Session response."""

    id: int
    store_code: str
    table_no: int
    started_at: datetime
    ended_at: datetime | None

    model_config = {"from_attributes": True}

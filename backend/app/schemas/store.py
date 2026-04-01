"""Store schemas — synced with Unit 1."""

from typing import Optional

from pydantic import BaseModel


class StoreResponse(BaseModel):
    store_code: str
    name: str
    address: Optional[str] = None
    phone: Optional[str] = None

    model_config = {"from_attributes": True}

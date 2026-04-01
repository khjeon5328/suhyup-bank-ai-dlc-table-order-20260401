"""Store schemas."""

from typing import Optional

from pydantic import BaseModel


class StoreResponse(BaseModel):
    id: int
    name: str
    code: str
    address: Optional[str] = None
    phone: Optional[str] = None

    model_config = {"from_attributes": True}

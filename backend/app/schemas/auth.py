"""Auth schemas — synced with Unit 1 (store_code based)."""

from typing import Optional

from pydantic import BaseModel, Field


class AdminLoginRequest(BaseModel):
    store_code: str = Field(..., min_length=1, max_length=20)
    username: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=1)


class TableLoginRequest(BaseModel):
    store_code: str = Field(..., min_length=1, max_length=20)
    table_no: int = Field(..., ge=1)
    password: str = Field(..., min_length=1)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: Optional[int] = None


class AdminLoginResponse(TokenResponse):
    user: "UserInfo"


class TableLoginResponse(TokenResponse):
    table: "TableInfo"


class UserInfo(BaseModel):
    id: int
    username: str
    role: str
    store_code: str


class TableInfo(BaseModel):
    store_code: str
    table_no: int
    session_id: int


class TokenPayload(BaseModel):
    user_id: Optional[int] = None
    table_no: Optional[int] = None
    store_code: str
    session_id: Optional[int] = None
    role: str  # owner, manager, table

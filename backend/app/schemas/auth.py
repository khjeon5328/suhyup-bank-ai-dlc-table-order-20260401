"""Auth schemas."""

from typing import Optional

from pydantic import BaseModel, Field


class AdminLoginRequest(BaseModel):
    store_code: str = Field(..., min_length=1, max_length=50)
    username: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=1)


class TableLoginRequest(BaseModel):
    store_code: str = Field(..., min_length=1, max_length=50)
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
    store_id: int


class TableInfo(BaseModel):
    id: int
    table_no: int
    store_id: int
    session_id: int


class TokenPayload(BaseModel):
    user_id: Optional[int] = None
    table_id: Optional[int] = None
    store_id: int
    session_id: Optional[int] = None
    role: str  # owner, manager, table

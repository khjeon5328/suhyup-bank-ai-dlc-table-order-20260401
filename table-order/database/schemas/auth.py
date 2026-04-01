"""Authentication schemas."""

from pydantic import BaseModel, Field


class AdminLoginRequest(BaseModel):
    """Admin login request."""

    store_code: str = Field(..., description="매장 코드")
    username: str = Field(..., description="사용자명")
    password: str = Field(..., description="비밀번호")


class TableLoginRequest(BaseModel):
    """Table tablet login request."""

    store_code: str = Field(..., description="매장 코드")
    table_no: int = Field(..., ge=1, description="테이블 번호")
    password: str = Field(..., description="테이블 PIN")


class TokenResponse(BaseModel):
    """JWT token response."""

    access_token: str
    token_type: str = "bearer"

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class LoginRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=50)
    model_config = ConfigDict(extra='forbid')


class LoginResponse(BaseModel):
    username: str
    name: str
    email: Optional[str] = Field(None, max_length=50)
    phone: Optional[str] = Field(None, pattern=r'^1[3-9]\d{9}$')
    avatar: Optional[str] = None
    status: int

    # 可以直接从 ORM 模型创建 Pydantic 模型
    model_config = ConfigDict(from_attributes=True, extra='forbid')


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=50)
    confirm_password: str = Field(min_length=6, max_length=50)
    name: str = Field(min_length=2, max_length=100)
    email: Optional[str] = Field(None, max_length=50)
    phone: Optional[str] = Field(None, pattern=r'^1[3-9]\d{9}$')

    model_config = ConfigDict(extra='forbid')

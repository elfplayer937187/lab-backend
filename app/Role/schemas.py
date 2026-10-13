from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class CreateRoleRequest(BaseModel):
    """创建角色请求体。"""

    name: str = Field(..., min_length=1, max_length=50, description='角色名')
    description: Optional[str] = Field(None, max_length=255, description='描述')
    status: Optional[Literal[0, 1]] = Field(default=1, description='状态: 0-禁用,1-启用')


class GetRoleListRequest(BaseModel):
    """获取角色列表请求体。"""

    page: int = Field(1, description='页码', gt=0)
    pageSize: int = Field(10, description='每页数量', gt=0, le=100)
    keyword: Optional[str] = Field('', description='关键字')


class GetRoleListResponse(CreateRoleRequest):
    """获取角色列表响应体。"""

    id: int
    # 从 ORM 对象(Role)直接构造,和 GetLabListResponse 同一套做法。
    model_config = ConfigDict(from_attributes=True)


class UpdateRoleRequest(CreateRoleRequest):
    """更新角色请求体。"""

    id: int = Field(..., ge=1)
    model_config = ConfigDict(extra='forbid')

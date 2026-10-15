from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class CreateMenuRequest(BaseModel):
    """创建菜单请求体。"""

    code: str = Field(..., description="权限标识")
    name: str = Field(..., description="权限名")
    pid: Optional[int | None] = Field(None, description="父级权限id")
    description: str = Field(max_length=255, description="描述")
    type: Literal[1, 2] = Field(..., description="权限类型: 1-菜单,2-按钮")
    status: Literal[0, 1] = Field(..., description="状态: 0-禁用,1-启用")


class CreateMenuResponse(CreateMenuRequest):
    id: int = Field(..., description="菜单id")

    model_config = ConfigDict(from_attributes=True)


class UpdateMenuRequest(CreateMenuResponse):
    """更新菜单请求体。"""


class MenuTreeResponse(CreateMenuResponse):
    """菜单树节点。"""

    children: list["MenuTreeResponse"] = Field(
        default_factory=list, description="子菜单"
    )

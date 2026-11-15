from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class CreateDeviceTypeRequest(BaseModel):
    """创建设备类型请求体。"""

    type_name: str = Field(..., min_length=1, max_length=30, description="设备类型名称")
    type_desc: Optional[str] = Field(None, max_length=100, description="设备类型描述")
    type_code: str = Field(..., min_length=1, max_length=30, description="设备类型编号")
    status: Literal[0, 1] = Field(1, description="状态: 0-禁用,1-启用")


class UpdateDeviceTypeRequest(CreateDeviceTypeRequest):
    """更新设备类型请求体。"""

    type_id: int = Field(..., ge=1)


class UpdateDeviceTypeStatusRequest(BaseModel):
    """启用/禁用设备类型请求体。"""

    type_id: int = Field(..., ge=1)
    status: Literal[0, 1]


class GetDeviceTypeListRequest(BaseModel):
    """设备类型分页查询参数。"""

    page: int = Field(1, ge=1, description="页码")
    # 上限 100 与用户列表一致:不设的话 pageSize 传很大就能一次拉全表
    pageSize: int = Field(10, ge=1, le=100, description="每页数量")
    keyword: Optional[str] = Field("", max_length=30, description="名称或编号关键字")
    # 查询参数从 query string 来,永远是字符串("1" 而不是 1)。
    # Literal[0, 1] 不做 str→int 转换,收到 "1" 直接校验失败;用 int + ge/le 才能兼容。
    status: Optional[int] = Field(None, ge=0, le=1, description="状态筛选")


class GetDeviceTypeResponse(CreateDeviceTypeRequest):
    """设备类型响应体。"""

    type_id: int
    model_config = ConfigDict(from_attributes=True)

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CreateLabDeviceRequest(BaseModel):
    """创建设备资料请求体。"""

    device_name: str = Field(..., min_length=1, max_length=30, description="设备名称")
    device_code: str = Field(..., min_length=1, max_length=30, description="设备编号")
    brand: str = Field(..., min_length=1, max_length=30, description="设备品牌")
    type_id: int = Field(..., ge=1, description="设备类型ID")
    description: Optional[str] = Field(None, max_length=100, description="设备描述")
    status: int = Field(1, description="状态: 0-禁用,1-启用")

    @field_validator("status")
    @classmethod
    def _validate_status(cls, value: int) -> int:  # noqa: N805
        if value not in (0, 1):
            raise ValueError("状态值只能为 0 或 1")
        return value

class UpdateLabDeviceRequest(CreateLabDeviceRequest):
    """更新设备资料请求体。"""

    lab_device_id: int = Field(..., ge=1)


class UpdateLabDeviceStatusRequest(BaseModel):
    """启用/禁用设备资料请求体。"""

    lab_device_id: int = Field(..., ge=1)
    status: Literal[0, 1]


class GetLabDeviceListRequest(BaseModel):
    """设备资料分页查询参数。"""

    page: int = Field(1, ge=1, description="页码")
    pageSize: int = Field(10, ge=1, le=100, description="每页数量")
    keyword: Optional[str] = Field("", max_length=30, description="名称或编号关键字")
    type_id: Optional[int] = Field(None, description="设备类型筛选")
    # 查询参数从 query string 来,永远是字符串("1" 而不是 1)。
    # Literal[0, 1] 不做 str→int 转换,收到 "1" 直接校验失败;用 int + ge/le 才能兼容。
    status: Optional[int] = Field(None, ge=0, le=1, description="状态筛选")


class GetLabDeviceResponse(CreateLabDeviceRequest):
    """设备资料响应体。"""

    lab_device_id: int
    effective_type: int | None
    model_config = ConfigDict(from_attributes=True)

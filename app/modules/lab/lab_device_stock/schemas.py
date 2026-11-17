from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CreateLabDeviceStockRequest(BaseModel):
    """给实验室添加设备请求体。"""

    lab_id: int = Field(..., ge=1, description="实验室ID")
    device_id: int = Field(..., ge=1, description="设备资料ID")
    quantity: int = Field(1, ge=0, description="设备数量")
    location: Optional[str] = Field(None, max_length=100, description="存放位置")
    remark: Optional[str] = Field(None, max_length=500, description="备注")


class UpdateLabDeviceStockRequest(BaseModel):
    """修改实验室设备请求体。id 定位记录,其余只提交要改的那几项。"""

    id: int = Field(..., ge=1, description="库存记录ID")
    quantity: Optional[int] = Field(None, ge=0, description="设备数量")
    available_quantity: Optional[int] = Field(None, ge=0, description="可用数量")
    location: Optional[str] = Field(None, max_length=100, description="存放位置")
    remark: Optional[str] = Field(None, max_length=500, description="备注")


class GetLabDeviceStockListRequest(BaseModel):
    """实验室设备列表查询参数。"""

    lab_id: int = Field(..., ge=1, description="实验室ID")
    page: int = Field(1, ge=1, description="页码")
    pageSize: int = Field(10, ge=1, le=100, description="每页数量")
    # keyword 同时匹配设备名称、编号、品牌;type_id 精确匹配设备类型
    keyword: Optional[str] = Field("", max_length=30, description="名称/编号/品牌关键字")
    type_id: Optional[int] = Field(None, ge=1, description="设备类型筛选")


class LabDeviceStockResponse(BaseModel):
    """实验室设备详情:库存信息 + 设备基础信息。"""

    id: int
    lab_id: int
    device_id: int
    quantity: int
    available_quantity: int
    location: Optional[str] = None
    remark: Optional[str] = None
    # 以下来自设备资料库(lab_device)和设备类型表(lab_device_type)
    device_name: str
    device_code: str
    brand: str
    type_id: int
    type_name: str
    device_status: int
    model_config = ConfigDict(from_attributes=True)

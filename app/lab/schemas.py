from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class CreateLabRequest(BaseModel):
    """创建实验室请求体。"""

    name: str
    description: Optional[str] = None
    capacity: Optional[int] = 0
    image: Optional[str] = None
    open_time: Optional[str] = None
    close_time: Optional[str] = None
    status: Optional[Literal[0, 1]] = Field(default=1)


class GetLabListRequest(BaseModel):
    """获取实验室请求体。"""

    page: int = Field(1, description="页码", gt=0)
    pageSize: int = Field(10, description="每页数量", gt=0)
    keyword: Optional[str] = Field("", description="关键字")


class GetLabListResponse(CreateLabRequest):
    """获取实验室列表响应体。"""

    id: int
    # 从 ORM 对象(Lab)直接构造,和 UserInfoResponse 同一套做法。
    # 不开这个,Pydantic 只认 dict,传 Lab 实例会报 model_type 校验错。
    model_config = ConfigDict(from_attributes=True)

class UpdateLabRequest(CreateLabRequest):
    """更新实验室请求体。"""

    id: int = Field(..., ge=1)

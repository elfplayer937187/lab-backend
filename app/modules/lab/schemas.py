from datetime import time
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class CreateLabRequest(BaseModel):
    """创建实验室请求体。"""

    name: str
    description: Optional[str] = None
    capacity: Optional[int] = 0
    image: Optional[str] = Field(None, description="图片")
    open_time: Optional[time] = Field(None, description="开放时间")
    close_time: Optional[time] = Field(None, description="结束时间")
    manager_id: int = Field(default=1)
    status: Optional[Literal[0, 1]] = Field(default=1)
    building: int = Field(description="所属楼层")
    floor: int = Field(description="所属楼层")
    area: int = Field(description="占地面积")


class GetLabListRequest(BaseModel):
    """获取实验室请求体。"""

    page: int = Field(1, description="页码", gt=0)
    pageSize: int = Field(10, description="每页数量", gt=0)
    nameKeyword: Optional[str] = Field("", description="关键字")
    building: Optional[int] = Field(None, description="所属楼层")
    floor: Optional[int] = Field(None, description="所属楼层")
    manage_id: Optional[int] = Field(None, description="管理员id")


class GetLabListResponse(CreateLabRequest):
    """获取实验室列表响应体。"""

    id: int
    # 从 ORM 对象(Lab)直接构造,和 UserInfoResponse 同一套做法。
    # 不开这个,Pydantic 只认 dict,传 Lab 实例会报 model_type 校验错。
    model_config = ConfigDict(from_attributes=True)


class UpdateLabRequest(CreateLabRequest):
    """更新实验室请求体。"""

    id: int = Field(..., ge=1)


class GetUserListResponse(BaseModel):
    """获取用户列表响应体。"""

    id: int
    username: str
    # 从 ORM 对象(User)直接构造,和 UserInfoResponse 同一套做法。
    # 不开这个,Pydantic 只认 dict,传 User 实例会报 model_type 校验错。
    model_config = ConfigDict(from_attributes=True)


class UpdateLabImageRequest(BaseModel):
    """更新实验室图片请求体。"""

    id: int = Field(..., ge=1)
    imageUrl: str

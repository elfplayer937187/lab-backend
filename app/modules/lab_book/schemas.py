from datetime import time
from typing import Optional, Self

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class CreateLabBookRequest(BaseModel):
    """创建实验室预约请求体。"""

    lab_id: int
    start_time: time
    end_time: time
    people_count: int

    @field_validator("start_time", "end_time")
    @classmethod
    def _reject_tz_aware(cls, v: time) -> time:
        """拒绝带时区偏移的时间。"""
        if v.tzinfo is not None:
            raise ValueError("时间不要带时区偏移,请传本地时间,如 09:00")
        return v

    @model_validator(mode="after")
    def _check_time_order(self) -> Self:
        """校验结束时间晚于开始时间。"""
        if self.start_time >= self.end_time:
            raise ValueError("结束时间必须晚于开始时间")
        return self


class LabBookListResponse(BaseModel):
    id: int
    username: str
    user_id: int
    lab_id: int
    start_time: time
    end_time: time
    people_count: int
    status: int
    reviewer_id: int
    reviewer_remark: Optional[str] = Field(None)

    model_config = ConfigDict(from_attributes=True)

from datetime import time
from typing import List

from pydantic import BaseModel, Field


class DashHomeShouldAcceptItem(BaseModel):
    """dashboard 待审批预约列表项。"""

    LabBookId: int
    LabName: str
    Username: str
    StartTime: time
    EndTime: time
    PeopleCount: int
    Status: int


class DashHomeDataResponse(BaseModel):
    LabClassTotalCount: int = Field(0, description="实验室班级总数")
    LabDeviceTotalCount: int = Field(0, description="实验室设备总数")
    ShouldAcceptTotalCount: int = Field(0, description="待审批预约总数")
    ShouldAcceptList: List[DashHomeShouldAcceptItem] = Field(
        default_factory=list, description="待审批预约列表"
    )

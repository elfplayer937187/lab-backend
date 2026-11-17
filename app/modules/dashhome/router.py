from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBearer
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.common.base_response import success_response
from app.database import get_db
from app.modules.dashhome.schemas import DashHomeDataResponse
from app.modules.lab.database import Lab
from app.modules.lab.lab_device.database import LabDevice
from app.modules.lab_book.database import LabBook
from app.modules.User.database import User

dashboard_router = APIRouter(prefix="/dashboard", tags=["首页"],dependencies=[Depends(HTTPBearer())])


@dashboard_router.get(
    "/data", summary="获取dashboard数据", description="获取dashboard数据"
)
def get_dashboard_data(request: Request, db: Session = Depends(get_db)):
    # 查询实验室总数
    LabClassTotalCount = db.scalar(select(func.count()).select_from(Lab))
    # 查询设备总数
    LabDeviceTotalCount = db.scalar(select(func.count()).select_from(LabDevice))
    # 查询待审核预约数
    ShouldAcceptTotalCount = db.scalar(
        select(func.count()).select_from(LabBook).where(LabBook.status == 0)
    ) or 0
    # 待审批预约列表:任意有权限的审批人看到的都是同一份(不再按 reviewer_id 过滤)
    ShouldAcceptList = (
        db.execute(
            select(
                LabBook.id,
                LabBook.start_time,
                LabBook.end_time,
                LabBook.people_count,
                LabBook.status,
                User.name.label("username"),
                Lab.name.label("lab_name"),
            )
            .join(User, LabBook.user_id == User.id)
            .join(Lab, LabBook.lab_id == Lab.id)
            .where(LabBook.status == 0)

            .order_by(LabBook.id.desc())
        )
        .mappings()
        .all()
    )
    return success_response(
        data=DashHomeDataResponse.model_validate(
            {
                "LabClassTotalCount": LabClassTotalCount,
                "LabDeviceTotalCount": LabDeviceTotalCount,
                "ShouldAcceptTotalCount": ShouldAcceptTotalCount,
                "ShouldAcceptList": [
                    {
                        "LabBookId": row["id"],
                        "LabName": row["lab_name"],
                        "Username": row["username"],
                        "StartTime": row["start_time"],
                        "EndTime": row["end_time"],
                        "PeopleCount": row["people_count"],
                        "Status": row["status"],
                    }
                    for row in ShouldAcceptList
                ],
            }
        )
    )

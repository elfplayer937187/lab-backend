# 是否能够预定
# 1.实验室开放时间
# 2.实验室预约人数<容量
# 3.是否冲突

from datetime import time

from fastapi import Depends
from numpy import bool_
from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.common.business_error import BusinessError
from app.database import get_db
from app.modules.lab.database import Lab
from app.modules.lab_book.database import LabBook


def is_in_open_time(
    start_time: time, end_time: time, lab_open_time: time, lab_close_time: time
):
    return start_time >= lab_open_time and end_time <= lab_close_time


def is_in_capacity(people_count: int, lab_capacity: int):
    return people_count <= lab_capacity


# 查询这个时间段是否有其他人预约了
def is_conflict_with_others(lab_id: int, start_time: time, end_time: time, db: Session):
    lab = db.scalar(
        select(Lab)
        .join(LabBook, Lab.id == LabBook.lab_id)
        .where(
            and_(
                Lab.id == lab_id,
                LabBook.start_time >= start_time,
                LabBook.end_time <= end_time,
            )
        )
    )
    return lab is not None


def is_conflict(
    lab_id: int,
    start_time: time,
    end_time: time,
    people_count: int,
    db: Session,
) -> bool:
    lab = db.get(Lab, lab_id)
    if lab is None:
        raise BusinessError()
    if not is_in_open_time(
        start_time=start_time,
        end_time=end_time,
        lab_open_time=lab.open_time or time(8, 0),
        lab_close_time=lab.close_time or time(20, 0),
    ):
        return True
    if not is_in_capacity(people_count=people_count, lab_capacity=lab.capacity):
        return True

    if is_conflict_with_others(
        lab_id=lab_id, start_time=start_time, end_time=end_time, db=db
    ):
        return True
    return False

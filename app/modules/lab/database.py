from datetime import time
from typing import Literal, Optional

from pydantic import ConfigDict
from sqlalchemy import Integer, String, Time
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Lab(Base):
    __tablename__ = "lab"
    __table_args__ = {"comment": "实验室表"}

    id: Mapped[int] = mapped_column(
        primary_key=True, unique=True, comment="主键", autoincrement=True
    )
    manager_id: Mapped[int] = mapped_column(comment="管理员id")
    name: Mapped[str] = mapped_column(String(10), comment="实验室名", unique=True)
    description: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True, comment="描述"
    )
    image: Mapped[Optional[str]] = mapped_column(
        String(70), nullable=True, comment="图片"
    )
    capacity: Mapped[int] = mapped_column(Integer, comment="容量", default=0)
    building: Mapped[int] = mapped_column(comment="所属楼层号")
    floor: Mapped[int] = mapped_column(comment="所属楼层")
    area: Mapped[int] = mapped_column(comment="占地面积(m2)")
    open_time: Mapped[Optional[time]] = mapped_column(
        Time, comment="开放时间", default=time(8, 0)
    )
    close_time: Mapped[Optional[time]] = mapped_column(
        Time, comment="结束时间", default=time(20, 0)
    )
    status: Mapped[Literal[0, 1]] = mapped_column(Integer, comment="状态", default=0)

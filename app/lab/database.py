from datetime import datetime
from typing import Literal, Optional

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Lab(Base):
    __tablename__ = "lab"
    __table_args__ = {"comment": "实验室表"}

    id: Mapped[int] = mapped_column(primary_key=True, comment="主键")
    name: Mapped[str] = mapped_column(String(10), comment="实验室名")
    description: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True, comment="描述"
    )
    image: Mapped[Optional[str]] = mapped_column(
        String(70), nullable=True, comment="图片"
    )
    capacity: Mapped[int] = mapped_column(Integer, comment="容量", default=0)
    open_time: Mapped[datetime] = mapped_column(
        DateTime, comment="开放时间", nullable=True
    )
    close_time: Mapped[datetime] = mapped_column(
        DateTime, comment="结束时间", nullable=True
    )
    status: Mapped[Literal["0", "1"]] = mapped_column(
        Integer, comment="状态", default=1
    )

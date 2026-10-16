from typing import Literal

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, time
from app.database import Base


class LabBook(Base):
    __tablename__ = "lab_book"
    __table_args__ = {"comment": "实验室预约表"}
    id: Mapped[int] = mapped_column(
        primary_key=True, unique=True, autoincrement=True, comment="主键"
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), comment="用户id", index=True
    )
    lab_id: Mapped[int] = mapped_column(comment="实验室id")
    start_time: Mapped[time] = mapped_column(comment="预约开始时间")
    end_time: Mapped[time] = mapped_column(comment="预约结束时间")
    people_count: Mapped[int] = mapped_column(comment="预约人数")
    status: Mapped[int] = mapped_column(
        comment="预约状态: 0-待审核,1-审核通过,2-,3-已取消"
    )

    reviewer_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        comment="审核人id",
        index=True,
        default=1,
    )
    reviewer_remark: Mapped[str | None] = mapped_column(
        String(255), nullable=True, comment="审核人备注"
    )


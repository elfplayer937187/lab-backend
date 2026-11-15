from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


# 实验室设备类型
class LabDeviceType(Base):
    __tablename__ = "lab_device_type"
    __table_args__ = {"comment": "实验室设备类型"}
    type_id: Mapped[int] = mapped_column(
        primary_key=True, comment="设备类型ID", autoincrement=True
    )
    type_name: Mapped[str] = mapped_column(
        String(30), comment="设备类型名称", unique=True, nullable=False
    )
    type_desc: Mapped[str] = mapped_column(
        String(100), comment="设备类型描述", nullable=True
    )
    type_code: Mapped[str] = mapped_column(
        String(30), comment="设备类型编号", unique=True, nullable=False
    )
    status: Mapped[int] = mapped_column(comment="设备类型状态", default=1)

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class LabDevice(Base):
    __tablename__ = "lab_device"
    __table_args__ = {"comment": "实验室设备"}

    lab_device_id: Mapped[int] = mapped_column(
        primary_key=True, comment="实验室设备ID", autoincrement=True
    )
    device_name: Mapped[str] = mapped_column(
        String(30),
        comment="设备名称",
        nullable=False,
    )
    device_code: Mapped[str] = mapped_column(
        String(30), comment="设备编号", nullable=False, unique=True
    )
    brand: Mapped[str] = mapped_column(String(30), comment="设备品牌", nullable=False)
    type_id: Mapped[int] = mapped_column(
        ForeignKey("lab_device_type.type_id"), comment="设备类型ID", nullable=False
    )
    description: Mapped[str] = mapped_column(
        String(100), comment="设备描述", nullable=True
    )
    status: Mapped[int] = mapped_column(comment="设备状态", default=1)

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


# 实验室设备关联表:记录哪个实验室拥有哪种设备、拥有多少
class LabDeviceStock(Base):
    __tablename__ = "lab_device_stock"
    __table_args__ = {"comment": "实验室设备关联表"}

    id: Mapped[int] = mapped_column(
        primary_key=True, comment="主键", autoincrement=True
    )
    lab_id: Mapped[int] = mapped_column(
        ForeignKey("lab.id"), comment="实验室ID", nullable=False
    )
    device_id: Mapped[int] = mapped_column(
        ForeignKey("lab_device.lab_device_id"), comment="具体设备ID", nullable=False
    )
    quantity: Mapped[int] = mapped_column(comment="设备数量", default=0)
    available_quantity: Mapped[int] = mapped_column(comment="可用数量", default=0)
    location: Mapped[str | None] = mapped_column(
        String(100), comment="存放位置", nullable=True
    )
    remark: Mapped[str | None] = mapped_column(
        String(500), comment="备注", nullable=True
    )

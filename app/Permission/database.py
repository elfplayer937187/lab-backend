from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Permission(Base):
    __tablename__ = "permission"
    __table_args__ = {"comment": "权限表"}

    id: Mapped[int] = mapped_column(
        primary_key=True, unique=True, autoincrement=True, comment="主键"
    )
    # code 是权限的业务标识,校验时按它判断(如 lab:create,user:list),不用自增 id。
    code: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        comment="权限标识: 如 lab:create,user:list",
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False, comment="权限名")
    description: Mapped[str | None] = mapped_column(
        String(255), nullable=True, comment="描述"
    )
    pid: Mapped[int | None] = mapped_column(comment="父级权限id")
    type: Mapped[int] = mapped_column(default=2, comment="权限类型: 1-菜单,2-按钮")
    status: Mapped[int] = mapped_column(default=1, comment="状态: 0-禁用,1-启用")

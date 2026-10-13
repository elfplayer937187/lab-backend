from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Role(Base):
    __tablename__ = 'role'
    __table_args__ = {'comment': '角色表'}

    id: Mapped[int] = mapped_column(
        primary_key=True, unique=True, autoincrement=True, comment='主键'
    )
    name: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, comment='角色名,可扩展: 学生/管理员/校长等'
    )
    description: Mapped[str | None] = mapped_column(String(255), nullable=True, comment='描述')
    status: Mapped[int] = mapped_column(default=1, comment='状态: 0-禁用,1-启用')

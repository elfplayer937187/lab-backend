from typing import Literal

from sqlalchemy import String
from sqlalchemy.orm import Mapped, deferred, mapped_column

from app.database import Base


class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'comment': '用户表'}

    # id 必须在这里声明,不能挪回 Base —— SQLAlchemy 会把继承来的列排到子类自己
    # 声明的列之后,那样建出来的表第一列就不是主键了。其他模型同理。
    id: Mapped[int] = mapped_column(
        primary_key=True, unique=True, autoincrement=True, comment='主键'
    )
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment='用户名')
    # bcrypt 哈希固定 60 字符,留出余量以便将来换 Argon2 等更长的算法
    password: Mapped[str] = deferred(mapped_column(String(100), nullable=False, comment='密码'))
    name: Mapped[str] = mapped_column(String(50), nullable=False, comment='姓名')
    email: Mapped[str | None] = mapped_column(String(50), nullable=True, comment='邮箱')
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True, comment='手机号')
    avatar: Mapped[str | None] = mapped_column(String(50), nullable=True, comment='头像')
    status: Mapped[int] = mapped_column(default=1, comment='状态: 0-禁用,1-启用')

    @property
    def is_active(self) -> bool:
        return self.status == 1


from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'comment': '用户表'}

    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment='用户名')
    # bcrypt 哈希固定 60 字符,留出余量以便将来换 Argon2 等更长的算法
    password: Mapped[str] = mapped_column(String(255), nullable=False, comment='密码哈希')
    name: Mapped[str] = mapped_column(String(50), nullable=False, comment='姓名')
    role: Mapped[str] = mapped_column(
        String(50), default='student', nullable=False, comment='角色: student-学生,admin-管理员'
    )
    email: Mapped[str | None] = mapped_column(String(50), nullable=True, comment='邮箱')
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True, comment='手机号')
    avatar: Mapped[str | None] = mapped_column(String(50), nullable=True, comment='头像')
    status: Mapped[int] = mapped_column(default=1, comment='状态: 0-禁用,1-启用')

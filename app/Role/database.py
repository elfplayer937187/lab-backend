from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Role(Base):
    __tablename__ = 'role'
    __table_args__ = {'comment': '角色表'}

    id: Mapped[int] = mapped_column(
        primary_key=True, unique=True, autoincrement=True, comment='主键'
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False, comment='角色名: 学生/管理员')
    # code 是角色的业务标识,取值与 User.role 列存的值一一对应(student/admin)。
    # User 表存字符串而非 role_id 外键,是因为这个值要进 JWT:换成自增 id 后,
    # 开发库与生产库的同一个角色不是同一个 id,token 跨环境即失效。
    code: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, comment='角色标识: student-学生,admin-管理员'
    )
    description: Mapped[str | None] = mapped_column(String(255), nullable=True, comment='描述')
    status: Mapped[int] = mapped_column(default=1, comment='状态: 0-禁用,1-启用')

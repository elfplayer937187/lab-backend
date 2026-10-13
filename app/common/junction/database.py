"""中间表(关联表)模型。

RBAC 里两张多对多关系的中间表集中在这里:
- user_role:        用户 ↔ 角色
- role_permission:  角色 ↔ 权限

中间表不另加自增 id:(user_id, role_id) 这类组合本身就是天然唯一键,直接当复合主键,
既省一列又顺带做了唯一约束。
"""

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class UserRole(Base):
    __tablename__ = 'user_role'
    __table_args__ = {'comment': '用户角色关联表'}

    user_id: Mapped[int] = mapped_column(
        ForeignKey('user.id', ondelete='CASCADE'), primary_key=True, comment='用户ID'
    )
    # 主键第一列 user_id 已自动建索引;role_id 单独索引,方便按角色反查用户。
    role_id: Mapped[int] = mapped_column(
        ForeignKey('role.id', ondelete='CASCADE'),
        primary_key=True,
        index=True,
        comment='角色ID',
    )


class RolePermission(Base):
    __tablename__ = 'role_permission'
    __table_args__ = {'comment': '角色权限关联表'}

    role_id: Mapped[int] = mapped_column(
        ForeignKey('role.id', ondelete='CASCADE'), primary_key=True, comment='角色ID'
    )
    permission_id: Mapped[int] = mapped_column(
        ForeignKey('permission.id', ondelete='CASCADE'),
        primary_key=True,
        index=True,
        comment='权限ID',
    )

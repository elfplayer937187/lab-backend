"""往 user 表插入开发用假数据。

用法(项目根目录执行,需先 `docker compose up -d`):
    .\\.venv\\Scripts\\python.exe scripts\\seed_users.py

幂等:按 username 判断,已存在的用户只更新密码/字段,不重复插入。
"""

import sys
from pathlib import Path

from sqlalchemy import select

# 直接 `python scripts/seed_users.py` 时 sys.path[0] 是 scripts/ 而非项目根,
# 这里补上根目录,免去每次设 PYTHONPATH。
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.database import SessionLocal  # noqa: E402
from app.models import Role, User, UserRole  # noqa: F401  通过 models 聚合入口确保表已注册
from app.utils.bcrypt import hash_password

# (username, password, name, role, email, phone)
# role 是 role.name 的外键关联(经 user_role 中间表),需先跑 seed_roles.py
SEED_USERS: list[tuple[str, str, str, str, str | None, str | None]] = [
    ('root', '123456', '超级管理员', '超级管理员', 'root@lab.local', '13800000000'),
    ('zhangsan', '123456', '张三', '学生', 'zhangsan@lab.local', '13800000001'),
    ('lisi', '123456', '李四', '学生', 'lisi@lab.local', '13800000002'),
]


def main() -> None:
    with SessionLocal() as session:
        for username, password, name, role, email, phone in SEED_USERS:
            hashed = hash_password(password)
            user = session.scalar(select(User).where(User.username == username))
            if user is None:
                user = User(
                    username=username,
                    password=hashed,
                    name=name,
                    email=email,
                    phone=phone,
                    status=1,
                )
                session.add(user)
                session.flush()  # 拿到自增 id 才能写 user_role
                print(f'[insert] {username} / {password}')
            else:
                # 已存在则重置密码,方便反复跑脚本后依然能登录
                user.password = hashed
                user.name = name
                user.email = email
                user.phone = phone
                user.status = 1
                print(f'[update] {username} / {password} (已存在,重置)')

            # 角色走 user_role 中间表,只保证「有」,不清理用户的其他角色
            role_obj = session.scalar(select(Role).where(Role.name == role))
            if role_obj is None:
                print(f'[skip] 角色「{role}」不存在,先跑 seed_roles.py')
            elif session.get(UserRole, (user.id, role_obj.id)) is None:
                session.add(UserRole(user_id=user.id, role_id=role_obj.id))
        session.commit()
    print('done')


if __name__ == '__main__':
    main()

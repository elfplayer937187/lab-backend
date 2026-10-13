"""往 role 表插入开发用假数据。

用法(项目根目录执行,需先 `docker compose up -d`):
    .\\.venv\\Scripts\\python.exe scripts\\seed_roles.py

幂等:按 name 判断,已存在的角色只更新描述/状态,不重复插入。
"""

import sys
from pathlib import Path

from sqlalchemy import select

# 直接 `python scripts/seed_roles.py` 时 sys.path[0] 是 scripts/ 而非项目根,
# 这里补上根目录,免去每次设 PYTHONPATH。
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.database import SessionLocal  # noqa: E402
from app.models import Role  # noqa: F401  通过 models 聚合入口确保表已注册

# (name, description, status)
SEED_ROLES: list[tuple[str, str, int]] = [
    ('超级管理员', '系统最高权限,不受权限表约束', 1),
    ('管理员', '实验室日常管理', 1),
    ('教师', '指导教师,可查看与管理自己名下的实验室', 1),
    ('学生', '普通学生,只读', 1),
    ('访客', '临时访客,只读', 0),
]


def main() -> None:
    with SessionLocal() as session:
        for name, description, status in SEED_ROLES:
            role = session.scalar(select(Role).where(Role.name == name))
            if role is None:
                session.add(Role(name=name, description=description, status=status))
                print(f'[insert] {name}')
            else:
                role.description = description
                role.status = status
                print(f'[update] {name} (已存在,重置)')
        session.commit()
    print('done')


if __name__ == '__main__':
    main()

"""往 lab_book 表插入开发用假数据。

用法(项目根目录执行,需先 `docker compose up -d`):
    .\\.venv\\Scripts\\python.exe scripts\\seed_lab_books.py

幂等:按 (user_id, lab_id, start_time) 判断,已存在的预约只更新其余字段,不重复插入。
用户取 seed_users.py 建出的 root / zhangsan / lisi,实验室取 seed_labs.py 的六条。
start_time / end_time 是 TIME 列,必须传 datetime.time,不能传 '09:00' 字符串。
"""

import sys
from datetime import time
from pathlib import Path

from sqlalchemy import select

# 直接 `python scripts/seed_lab_books.py` 时 sys.path[0] 是 scripts/ 而非项目根,
# 这里补上根目录,免去每次设 PYTHONPATH。
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.database import SessionLocal  # noqa: E402
from app.models import Lab, LabBook, User  # noqa: F401  通过 models 聚合入口确保表已注册

# (用户名, 实验室名, 开始, 结束, 人数, 状态, 审核备注)
# 状态: 0-待审核 1-审核通过 2-已驳回 3-已取消
SEED_LAB_BOOKS: list[tuple[str, str, time, time, int, int, str | None]] = [
    ('zhangsan', '人工智能实验室', time(9, 0), time(11, 0), 20, 1, '通过,注意设备使用规范'),
    ('zhangsan', '人工智能实验室', time(14, 0), time(16, 0), 15, 0, None),
    ('lisi', '大数据实验室', time(10, 0), time(12, 0), 30, 1, None),
    ('lisi', '物联网实验室', time(13, 30), time(15, 30), 12, 2, '人数超出该实验室当日容量'),
    ('zhangsan', '网络安全实验室', time(15, 0), time(17, 0), 10, 3, '学生自行取消'),
    ('lisi', '人工智能实验室', time(18, 0), time(20, 0), 8, 0, None),
    ('root', '云计算实验室', time(8, 0), time(10, 0), 25, 1, '管理员课程占用'),
    ('root', '软件工程实验室', time(9, 30), time(11, 30), 40, 0, None),
]


def main() -> None:
    with SessionLocal() as session:
        for username, lab_name, start, end, people, status, remark in SEED_LAB_BOOKS:
            user = session.scalar(select(User).where(User.username == username))
            lab = session.scalar(select(Lab).where(Lab.name == lab_name))
            if user is None or lab is None:
                print(f'[skip] {username} / {lab_name} 缺用户或实验室,先跑 seed_users.py、seed_labs.py')
                continue

            book = session.scalar(
                select(LabBook).where(
                    LabBook.user_id == user.id,
                    LabBook.lab_id == lab.id,
                    LabBook.start_time == start,
                )
            )
            if book is None:
                session.add(
                    LabBook(
                        user_id=user.id,
                        lab_id=lab.id,
                        start_time=start,
                        end_time=end,
                        people_count=people,
                        status=status,
                        reviewer_id=1,
                        reviewer_remark=remark,
                    )
                )
                print(f'[insert] {username} @ {lab_name} {start}-{end}')
            else:
                book.end_time = end
                book.people_count = people
                book.status = status
                book.reviewer_remark = remark
                print(f'[update] {username} @ {lab_name} {start}-{end} (已存在,重置)')
        session.commit()
    print('done')


if __name__ == '__main__':
    main()

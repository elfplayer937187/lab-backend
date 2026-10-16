"""往 lab 表插入开发用假数据。

用法(项目根目录执行,需先 `docker compose up -d`):
    .\\.venv\\Scripts\\python.exe scripts\\seed_labs.py

幂等:按 name 判断,已存在的实验室只更新其余字段,不重复插入。
manager_id 复用 scripts/seed_users.py 建出的用户(root=1、zhangsan=2、lisi=3)。
open_time / close_time 是 TIME 列,必须传 datetime.time,不能传 '08:00' 字符串。
"""

import sys
from datetime import time
from pathlib import Path

from sqlalchemy import select

# 直接 `python scripts/seed_labs.py` 时 sys.path[0] 是 scripts/ 而非项目根,
# 这里补上根目录,免去每次设 PYTHONPATH。
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.database import SessionLocal  # noqa: E402
from app.models import Lab  # noqa: F401  通过 models 聚合入口确保表已注册

# (name, manager_id, description, image, capacity, building, floor, area, open_time, close_time, status)
SEED_LABS: list[tuple[str, int, str, str | None, int, int, int, int, time, time, int]] = [
    (
        '人工智能实验室',
        1,
        '面向机器学习与深度学习研究,配备 GPU 服务器',
        'uploads/lab/ai.jpg',
        30,
        1,
        3,
        120,
        time(8, 0),
        time(22, 0),
        1,
    ),
    (
        '大数据实验室',
        1,
        '数据挖掘与可视化教学使用',
        'uploads/lab/bigdata.jpg',
        40,
        1,
        4,
        150,
        time(8, 30),
        time(21, 0),
        1,
    ),
    (
        '网络安全实验室',
        2,
        '攻防演练与渗透测试实训环境',
        None,
        20,
        2,
        2,
        90,
        time(9, 0),
        time(20, 0),
        1,
    ),
    (
        '物联网实验室',
        2,
        '传感器与嵌入式开发平台',
        'uploads/lab/iot.jpg',
        25,
        2,
        3,
        100,
        time(8, 0),
        time(18, 0),
        1,
    ),
    (
        '云计算实验室',
        3,
        '虚拟化与容器编排实验,支持远程接入',
        None,
        35,
        3,
        1,
        200,
        time(0, 0),
        time(23, 59),
        1,
    ),
    (
        '软件工程实验室',
        3,
        '敏捷开发与项目管理实训,暂未开放',
        None,
        45,
        3,
        5,
        160,
        time(8, 0),
        time(18, 0),
        0,
    ),
]


def main() -> None:
    with SessionLocal() as session:
        for (
            name,
            manager_id,
            description,
            image,
            capacity,
            building,
            floor,
            area,
            open_time,
            close_time,
            status,
        ) in SEED_LABS:
            lab = session.scalar(select(Lab).where(Lab.name == name))
            if lab is None:
                session.add(
                    Lab(
                        manager_id=manager_id,
                        name=name,
                        description=description,
                        image=image,
                        capacity=capacity,
                        building=building,
                        floor=floor,
                        area=area,
                        open_time=open_time,
                        close_time=close_time,
                        status=status,
                    )
                )
                print(f'[insert] {name}')
            else:
                lab.manager_id = manager_id
                lab.description = description
                lab.image = image
                lab.capacity = capacity
                lab.building = building
                lab.floor = floor
                lab.area = area
                lab.open_time = open_time
                lab.close_time = close_time
                lab.status = status
                print(f'[update] {name} (已存在,重置)')
        session.commit()
    print('done')


if __name__ == '__main__':
    main()

"""模型聚合入口。

SQLAlchemy 靠 import 的副作用把表注册到 Base.metadata:只有模型类所在的模块
被 import 过,`class Xxx(Base)` 才会执行,该表才会出现在 Base.metadata.tables 里。

`Base.metadata.create_all()` 只是遍历 Base.metadata.tables 发 CREATE TABLE,
遍历到空集合就静默什么都不做(不报错)。将来 alembic 的 env.py 也需要一个
「把所有模型导全」的入口,否则 autogenerate 会漏表。

⚠️ 新增模型模块时,务必在这里追加一行导入。
"""

from app.Role.database import Role
from app.User.database import User

__all__ = ['User', 'Role']

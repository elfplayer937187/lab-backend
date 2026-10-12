from logging.config import fileConfig

from sqlalchemy import create_engine, pool

import app.models  # noqa: F401  导入副作用:把全部模型注册进 Base.metadata
from alembic import context
from app.config import settings
from app.database import Base

# Alembic 的 Config 对象,对应 alembic.ini
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# autogenerate 的比对目标。app.models 必须被导入过,否则这里是个空集合,
# 生成的迁移会漏表(app.models 内部已聚合导入所有模型模块)。
target_metadata = Base.metadata


def get_url() -> str:
    """连接串从 app.config.settings 取,不写进 alembic.ini。

    写进 alembic.ini 等于把数据库密码提交进 git。同理,这里不用
    config.set_main_option:configparser 会把连接串里的 '%' 当插值符,
    密码含 '%' 时直接报错。直接拿字符串建 engine 绕开这个坑。
    """
    return settings.DATABASE_URL


def run_migrations_offline() -> None:
    """离线模式:只生成 SQL 文本,不连数据库。"""
    context.configure(
        url=get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """在线模式:连上数据库执行迁移。"""
    connectable = create_engine(get_url(), poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

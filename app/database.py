from collections.abc import Generator
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

from app.config import settings

# 同步引擎(pymysql 是同步驱动,不能用 create_async_engine)
# pool_pre_ping:连接取出前先探活,避免 MySQL 主动断开后拿到失效连接
engine = create_engine(settings.DATABASE_URL, echo=settings.DB_ECHO, pool_pre_ping=True)

# 同步会话工厂
SessionLocal = sessionmaker(bind=engine, class_=Session, expire_on_commit=False)


# 模型基类
class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True,comment="主键")
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now(), comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.now(), onupdate=datetime.now(), comment="更新时间"
    )


# 获取数据库会话依赖
def get_db() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise

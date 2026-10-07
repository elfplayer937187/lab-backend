from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

import app.models  # noqa: F401  必须先导入模型,否则 Base.metadata 是空的
from app.auth.router import router as auth_router
from app.common.business_error import BusinessError
from app.database import Base, engine
from app.filters.filters import (
    BusinessErrorHandler,
    RequestValidationErrorHandler,
    UnhandledErrorHandler,
)

# 创建数据库表。
# 只建「不存在」的表,不会修改已存在的表结构 —— 改字段要靠 alembic 迁移,
# 引入 alembic 后应删掉这一行。
Base.metadata.create_all(bind=engine)

app = FastAPI(title='FastAPI-Admin', description='FastAPI Admin', version='0.1.0')
app.include_router(auth_router)

app.add_exception_handler(BusinessError, BusinessErrorHandler)  # type: ignore[arg-type]
app.add_exception_handler(RequestValidationError, RequestValidationErrorHandler)  # type: ignore[arg-type]
app.add_exception_handler(Exception, UnhandledErrorHandler)


@app.get('/')
async def root():
    return {'message': 'Hello World'}

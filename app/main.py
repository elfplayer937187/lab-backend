from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from app.config import UPLOAD_DIR
import app.models  # noqa: F401  必须先导入模型,否则 Base.metadata 是空的
from app.__init__ import apiRouter
from app.common.business_error import BusinessError
from app.database import Base, engine
from app.filters.filters import (
    BusinessErrorHandler,
    RequestValidationErrorHandler,
    UnhandledErrorHandler,
)
from app.config import UPLOAD_DIR
from app.middlewares.jwt_midware import JWTMiddleWare
from pathlib import Path

# 创建数据库表。
# 只建「不存在」的表,不会修改已存在的表结构 —— 改字段要靠 alembic 迁移,
# 引入 alembic 后应删掉这一行。
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI-Admin", description="FastAPI Admin", version="0.1.0")
app.include_router(apiRouter)

app.add_exception_handler(BusinessError, BusinessErrorHandler)  # type: ignore[arg-type]
app.add_exception_handler(RequestValidationError, RequestValidationErrorHandler)  # type: ignore[arg-type]
app.add_exception_handler(Exception, UnhandledErrorHandler)

app.add_middleware(JWTMiddleWare)

if not Path(UPLOAD_DIR).exists():
    Path(UPLOAD_DIR).mkdir(parents=True)

app.mount("/uploads", StaticFiles(directory=f"{UPLOAD_DIR}"), name="uploads")



@app.get("/")
async def root():
    return {"message": "Hello World"}

import logging

from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from app.config import UPLOAD_DIR
from app.__init__ import apiRouter
from app.common.business_error import BusinessError
from app.filters.filters import (
    BusinessErrorHandler,
    RequestValidationErrorHandler,
    UnhandledErrorHandler,
)
from app.config import UPLOAD_DIR
from app.middlewares.jwt_midware import JWTMiddleWare
from pathlib import Path

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.warning("Starting up...")
    yield
    logger.warning("Shutting down...")


app = FastAPI(
    title="FastAPI-Admin",
    description="FastAPI Admin",
    version="0.1.0",
    swagger_ui_parameters={"persistAuthorization": True},
    lifespan=lifespan,
)
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

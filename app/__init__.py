from fastapi import APIRouter
from app.auth.router import router as auth_router
from app.upload.upload_config import file_router
from app.User.router import user_router

apiRouter = APIRouter(prefix="/api")

apiRouter.include_router(auth_router)
apiRouter.include_router(file_router)
apiRouter.include_router(user_router)

from fastapi import APIRouter

from app.auth.router import router as auth_router
from app.modules.ai_chat.router import ai_router
from app.modules.lab.lab_device.router import lab_device_router
from app.modules.lab.lab_device_type.router import device_type_router
from app.modules.lab.router import lab_router
from app.modules.lab_book.router import lab_book_router
from app.modules.Permission.router import menu_router
from app.modules.Role.router import role_router
from app.modules.User.router import user_router
from app.upload.upload_config import file_router
from app.modules.dashhome.router import dashboard_router
from app.common.test import test_router
apiRouter = APIRouter(prefix="/api")


apiRouter.include_router(test_router)
apiRouter.include_router(dashboard_router)
apiRouter.include_router(auth_router)
apiRouter.include_router(file_router)
apiRouter.include_router(user_router)
apiRouter.include_router(role_router)
apiRouter.include_router(menu_router)
# 实验室
apiRouter.include_router(lab_router)
# 实验室设备类型
apiRouter.include_router(device_type_router)
# 实验室设备资料
apiRouter.include_router(lab_device_router)
apiRouter.include_router(lab_book_router)
# ai
apiRouter.include_router(ai_router)

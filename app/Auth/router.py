from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.schemas import LoginRequest
from app.common.base_response import success_response
from app.common.business_error import BusinessError
from app.common.error_code import Code
from app.database import get_db
from app.User.database import User
from app.utils.bcrypt import verify_password

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/login', description='用户登录', summary='用户登录')
async def login(LoginInfo: LoginRequest, db: Session = Depends(get_db)):
    stmt = select(User).where(User.username == LoginInfo.username)
    user = db.execute(stmt).scalar_one_or_none()
    # 用户不存在 或者 密码错误。
    # 两种情况刻意合并成同一个响应:分开提示等于告诉攻击者哪些用户名真实存在(账号枚举)。
    # message 也不能写成「用户不存在」—— 密码错时那句话是假的,前端弹出来会误导用户。
    # http_status 显式传 401:USER_NOT_EXIST 的兜底映射是 404(用于查用户详情),
    # 但登录失败的 HTTP 语义是「认证未通过」。
    if not user or not verify_password(LoginInfo.password, user.password):
        raise BusinessError(code=Code.USER_NOT_EXIST, message='用户名或密码错误', http_status=401)

    if user.status != 1:
        raise BusinessError(code=Code.USER_DISABLED, message='用户被禁用', http_status=403)
    return success_response(
        data={
            'username': user.username,
            'name': user.name,
            'role': user.role,
            'email': user.email,
            'phone': user.phone,
            'avatar': user.avatar,
            'status': user.status,
        }
    )

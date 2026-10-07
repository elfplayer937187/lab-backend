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
    # 用户不存在 或者 密码错误
    if not user or not verify_password(LoginInfo.password, user.password):
        raise BusinessError(code=Code.USER_NOT_EXIST, message='用户不存在')

    if user.status != 1:
        raise BusinessError(code=Code.USER_NOT_EXIST, message='用户被禁用')
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

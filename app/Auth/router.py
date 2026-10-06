from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.schemas import LoginRequest
from app.common.base_response import error_response, success_response
from app.database import get_db
from app.User.database import User

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/login',description='用户登录',summary='用户登录')
async def login(LoginInfo: LoginRequest, db: Session = Depends(get_db)):
    stmt = select(User).where(
        User.username == LoginInfo.username, User.password == LoginInfo.password
    )
    user = db.execute(stmt).scalar_one_or_none()
    if not user:
        return error_response(code=401, message='用户名或密码错误')
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

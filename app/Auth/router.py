from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.schemas import LoginRequest, RegisterRequest
from app.common.base_response import success_response
from app.common.business_error import BusinessError
from app.common.error_code import Code
from app.database import get_db
from app.modules.User.database import User
from app.utils.bcrypt import hash_password, verify_password
from app.utils.jwt import create_access_token

router = APIRouter(prefix='/auth', tags=['用户登录注册'])


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
    token = create_access_token(user.id, user.username)
    return success_response(
        data={
            'id': user.id,
            'username': user.username,
            'name': user.name,
            'email': user.email,
            'phone': user.phone,
            'avatar': user.avatar,
            'status': user.status,
            'token': token,
        }
    )


@router.post('/register', description='用户注册', summary='用户注册')
async def register(RegisterInfo: RegisterRequest, db: Session = Depends(get_db)):
    stmt = select(User).where(User.username == RegisterInfo.username)
    user = db.execute(stmt).scalar_one_or_none()
    if user:
        raise BusinessError(code=Code.ACCOUNT_SAME, message='用户名已存在', http_status=409)
    if RegisterInfo.confirm_password != RegisterInfo.password:
        raise BusinessError(code=Code.PARAM_ERROR, message='密码不一致')
    user = User(
        username=RegisterInfo.username,
        password=hash_password(RegisterInfo.password),
        name=RegisterInfo.name or '未知',
        email=RegisterInfo.email or '',
        phone=RegisterInfo.phone or '',
        status=1,
    )
    db.add(user)
    return success_response(message='注册成功')

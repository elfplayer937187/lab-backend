from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.common.base_response import success_response
from app.common.business_error import BusinessError
from app.common.error_code import Code
from app.database import get_db
from app.User.database import User
from app.User.schemas import UpdateUserRequest, UserInfoResponse

user_router = APIRouter(prefix="/user", tags=["用户管理"])


@user_router.put("/update", description="修改个人资料", summary="修改个人资料")
def update_user(
    payload: UpdateUserRequest, request: Request, db: Session = Depends(get_db)
):
    """修改当前登录用户自己的资料。

    同步函数,不是 async:里面全是阻塞的 DB I/O。FastAPI 会自动把同步路由丢进
    线程池,写成 async 反而会占住事件循环(见 CLAUDE.md 第 6 节的异步约定)。
    """
    # user_id 取自 token,不取自请求体 —— 否则前端传谁的 id 就能改谁的资料。
    # 这个接口不在 JWTMiddleWare 的 WHITE_LIST 里,能走到这里说明中间件已验签通过
    # 并写好了 request.state。
    user = db.get(User, request.state.user_id)
    if user is None:
        # 验签通过但库里查不到人:用户被删了,或签名密钥被换过。
        raise BusinessError(code=Code.USER_NOT_EXIST, message="用户不存在")

    # 中间件只验签名和有效期,不查库,所以拦不住「账号已被禁用」:禁用一个用户后,
    # 他手里那个还没过期的 token 照样能调接口。登录接口自己查了 status,其余每个
    # 需要登录的接口都得补这道检查。
    if not user.is_active:
        raise BusinessError(
            code=Code.USER_DISABLED, message="用户被禁用", http_status=403
        )

    # exclude_unset 只写显式传上来的字段,exclude_none 顺手挡掉显式 null
    # (name 列是 NOT NULL,写进 None 会抛 IntegrityError → 500)。
    # setattr 对任意字段名都成立,安全性由 UpdateUserRequest 兜底:extra='forbid'
    # 已挡住 role / status / password 这些没声明的字段,传了就是 422。
    for field, value in payload.model_dump(
        exclude_unset=True, exclude_none=True
    ).items():
        setattr(user, field, value)

    # 这里不 commit:get_db 依赖在请求正常结束时统一 commit,异常时 rollback。
    # updated_at 由 Base 上的 onupdate=datetime.now 自动刷新,不用手动赋值。
    return success_response(message="修改成功")


# 获取用户信息接口
@user_router.get("/getInfo")
def get_user_info(request: Request, db: Session = Depends(get_db)):
    user_id = request.state.user_id
    stmt = select(User).where(User.id == user_id)
    user = db.execute(stmt).scalar_one_or_none()
    if not user:
        raise BusinessError(code=Code.USER_NOT_EXIST, message="用户不存在")
    return success_response(data=UserInfoResponse.model_validate(user))

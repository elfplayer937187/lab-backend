from typing import Annotated
from xml.etree.ElementInclude import include

from fastapi import APIRouter, Depends, Query, Request
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from sqlalchemy import delete, func, or_, select

from app.Role.database import Role
from app.common.base_response import PaginationResponse, success_response
from app.common.business_error import BusinessError
from app.common.error_code import Code
from app.common.junction.database import UserRole
from app.database import get_db
from app.User.database import User
from app.User.schemas import (
    AllRolesResponse,
    AssignRoleRequest,
    CreateUserRequest,
    ListUserRequest,
    UpdateUserByIdRequest,
    UpdateUserRequest,
    UpdateUserStatusRequest,
    UserInfoResponse,
    UserListItemResponse,
)
from app.utils.bcrypt import hash_password

api_bearer = HTTPBearer()

user_router = APIRouter(
    prefix="/user", tags=["用户管理"], dependencies=[Depends(api_bearer)]
)


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
    # 已挡住  status / password 这些没声明的字段,传了就是 422。
    for field, value in payload.model_dump(
        exclude_unset=True, exclude_none=True
    ).items():
        setattr(user, field, value)

    # 这里不 commit:get_db 依赖在请求正常结束时统一 commit,异常时 rollback。
    # updated_at 由 Base 上的 onupdate=datetime.now 自动刷新,不用手动赋值。
    return success_response(message="修改成功")


# 获取用户信息接口
@user_router.get("/getInfo", summary="获取用户信息", description="获取用户信息")
def get_user_info(request: Request, db: Session = Depends(get_db)):
    user_id = request.state.user_id
    stmt = select(User).where(User.id == user_id)
    user = db.execute(stmt).scalar_one_or_none()
    if not user:
        raise BusinessError(code=Code.USER_NOT_EXIST, message="用户不存在")
    return success_response(data=UserInfoResponse.model_validate(user))


@user_router.post("/create", summary="创建用户", description="创建用户")
def create_user(
    request: Request, create_dto: CreateUserRequest, db: Session = Depends(get_db)
):
    stmt = select(User).where(User.username == create_dto.username)
    user = db.execute(stmt).scalar_one_or_none()
    if user:
        raise BusinessError(code=Code.ACCOUNT_SAME, message="用户已存在")
    new_user = User(
        username=create_dto.username,
        password=hash_password(create_dto.password),
        name=create_dto.name,
        email=create_dto.email,
        phone=create_dto.phone,
    )

    db.add(new_user)

    return success_response(message="创建成功")


# 修改指定用户
@user_router.put("/updateById", summary="修改指定用户", description="修改指定用户")
def update_user_by_id(payload: UpdateUserByIdRequest, db: Session = Depends(get_db)):
    """按 id 修改任意用户,放开了 status / password。

    与 /update(改自己)的区别:id 来自请求体而不是 token;字段范围更大。
    目前没有管理员校验,任何登录用户都能调 —— 加权限时在这里补。
    """
    user = db.get(User, payload.id)
    if user is None:
        raise BusinessError(code=Code.USER_NOT_EXIST, message="用户不存在")

    data = payload.model_dump(exclude_unset=True, exclude_none=True, exclude={"id"})

    # password 是唯一「写入前必须变形」的字段:库里存的是 bcrypt 哈希,
    # 直接 setattr 明文进去等于把密码换成明文,之后 verify_password 全对不上。
    password = data.pop("password", None)
    if password is not None:
        user.password = hash_password(password)

    for field, value in data.items():
        setattr(user, field, value)

    return success_response(message="修改成功")


# 启用 / 禁用用户
@user_router.put(
    "/updateStatus", summary="启用或禁用用户", description="启用或禁用用户"
)
def update_user_status(payload: UpdateUserStatusRequest, db: Session = Depends(get_db)):
    user = db.get(User, payload.id)
    if user is None:
        raise BusinessError(code=Code.USER_NOT_EXIST, message="用户不存在")

    user.status = payload.status

    return success_response(message="操作成功")


# 分页查询用户
@user_router.get("/list", summary="分页查询用户", description="分页查询用户")
def list_users(
    payload: Annotated[ListUserRequest, Query()], db: Session = Depends(get_db)
):
    """按关键字分页查询用户,返回 {total, page, pageSize, data}。

    payload 是个 Pydantic 模型,但 Annotated[..., Query()] 把它声明成了查询参数,
    不是请求体 —— GET 带 body 会被不少客户端/代理直接丢掉,必须走 query string。

    不分页之外的筛选只有 keyword:同时模糊匹配 username 和 name,不传则返回全部。
    """
    conditions = []
    if payload.keyword:
        # 参数化绑定由 SQLAlchemy 的 like() 负责,不做字符串拼 SQL —— 否则是注入。
        like = f"%{payload.keyword}%"
        conditions.append(or_(User.username.like(like), User.name.like(like)))

    # total 必须单独 count 一次,不能拿 len(users) 顶替:那是当前页的条数,不是总数。
    total = db.scalar(select(func.count()).select_from(User).where(*conditions))

    # 所有角色
    stmt = (
        select(User)
        .where(*conditions)
        # 显式排序:不写 order_by 时 MySQL 不保证返回顺序,
        # 翻页会出现同一条记录重复或漏掉。
        .order_by(User.id.asc())
        .offset((payload.page - 1) * payload.pageSize)
        .limit(payload.pageSize)
    )
    users = db.execute(stmt).scalars().all()

    # 连表查已启用和已禁用的角色都带上:展示的是"他实际拥有什么",

    role_rows = db.execute(
        select(UserRole.user_id, Role.name)
        .join(Role, Role.id == UserRole.role_id)
        .where(UserRole.user_id.in_([user.id for user in users]))
        # 不写 order_by 时 MySQL 不保证顺序,角色名的排列会随机变化
        .order_by(UserRole.user_id, Role.id)
    ).all()
    roles_map: dict[int, list[str]] = {}
    for user_id, role_name in role_rows:
        roles_map.setdefault(user_id, []).append(role_name)

    records = []
    
    for user in users:
        item = UserListItemResponse.model_validate(user)
        item.roles = roles_map.get(user.id, [])
        records.append(item)

    return success_response(
        data=PaginationResponse(
            records=records,
            total=total or 0,
            page=payload.page,
            pageSize=payload.pageSize,
        )
    )


@user_router.delete("/delete", summary="删除用户", description="删除用户")
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.get(User, id)
    if user is None:
        raise BusinessError(code=Code.USER_NOT_EXIST, message="用户不存在")
    db.delete(user)
    return success_response(message="删除成功")


# 分配角色
@user_router.post("/assign_role", summary="分配角色", description="分配角色")
def assign_role(payload: AssignRoleRequest, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.id == payload.userId))
    if not user:
        raise BusinessError(
            code=Code.USER_NOT_EXIST,
            message="用户不存在",
            http_status=Code.USER_NOT_EXIST,
        )
    all_role_ids = db.scalars(select(Role.id)).all()

    if any(role_id not in all_role_ids for role_id in payload.roleId):
        raise BusinessError(
            code=Code.ROLE_NOT_EXIST,
            message="角色不存在",
            http_status=Code.ROLE_NOT_EXIST,
        )
    # 先清除已有角色
    stmt = delete(UserRole).where(UserRole.user_id == payload.userId)
    db.execute(stmt)
    # 批量加入角色
    db.add_all(
        [
            UserRole(user_id=payload.userId, role_id=role_id)
            for role_id in payload.roleId
        ]
    )
    return success_response(message="成功")


# 获取所有角色
@user_router.get(
    "/getAllRoles/{userId}", summary="获取所有角色", description="获取所有角色"
)
def get_role_list(userId: int, request: Request, db: Session = Depends(get_db)):
    # 获取用户已拥有的角色id
    haved_role = set(
        db.scalars(select(UserRole.role_id).where(UserRole.user_id == userId)).all()
    )
    # 获取所有启用中的角色,并标记用户是否已拥有
    all_role = db.execute(select(Role.id, Role.name).where(Role.status == 1)).all()
    return success_response(
        data=[
            {"id": role_id, "name": name, "check": role_id in haved_role}
            for role_id, name in all_role
        ],
        message="成功",
    )

from typing import Annotated
from fastapi import APIRouter, Depends, Query, Request
from fastapi.security import HTTPBearer
import rich
from sqlalchemy import delete, func, insert, select
from sqlalchemy.orm import Session

from app.common.base_response import pagination_response, success_response
from app.common.business_error import BusinessError
from app.common.error_code import Code
from app.common.junction.database import RolePermission
from app.database import get_db
from app.modules.Permission.database import Permission
from app.modules.Permission.services import get_tree_menu
from app.modules.Role.database import Role
from app.modules.Role.schemas import (
    AssignPermissionRequest,
    CreateRoleRequest,
    GetRoleListRequest,
    GetRoleListResponse,
    UpdateRoleRequest,
)

bearer = HTTPBearer()
role_router = APIRouter(
    prefix="/role", tags=["角色管理"], dependencies=[Depends(bearer)]
)


@role_router.post("/create", summary="创建角色", description="创建角色")
def create_role(payload: CreateRoleRequest, db: Session = Depends(get_db)):
    # name 建了唯一约束,先查一次给个友好的业务错误,而不是等 DB 抛 IntegrityError
    if db.scalar(select(Role).where(Role.name == payload.name)):
        raise BusinessError(code=Code.ROLE_EXIST, message="角色已存在")
    db.add(Role(**payload.model_dump()))
    return success_response().model_dump()


@role_router.get("/list", summary="获取角色列表", description="获取角色列表")
def get_role_list(
    payload: Annotated[GetRoleListRequest, Query()], db: Session = Depends(get_db)
):
    conditions = []
    # 拼接字符串防止注入
    if payload.keyword:
        like = f"%{payload.keyword}%"
        conditions.append(Role.name.like(like))
    total = db.scalar(select(func.count()).select_from(Role).where(*conditions))
    stmt = (
        select(Role)
        .where(*conditions)
        .limit(payload.pageSize)
        .offset((payload.page - 1) * payload.pageSize)
        .order_by(Role.id.asc())
    )
    roles = db.execute(stmt).scalars().all()
    return success_response(
        data=pagination_response(
            total=total or 0,
            page=payload.page,
            page_size=payload.pageSize,
            records=[GetRoleListResponse.model_validate(role) for role in roles],
        ),
        message="成功",
    )


@role_router.put("/update", summary="更新角色", description="更新角色")
def update_role(payload: UpdateRoleRequest, db: Session = Depends(get_db)):
    role = db.get(Role, payload.id)
    if role is None:
        raise BusinessError(code=Code.ROLE_NOT_EXIST, message="角色不存在")
    update_data = payload.model_dump(
        exclude_unset=True, exclude={"id"}, exclude_none=True
    )
    for key, value in update_data.items():
        setattr(role, key, value)
    return success_response()


@role_router.delete("/delete/{roleId}", summary="删除角色", description="删除角色")
def delete_role(roleId: int, db: Session = Depends(get_db)):
    role = db.get(Role, roleId)
    if role is None:
        raise BusinessError(code=Code.ROLE_NOT_EXIST, message="角色不存在")
    # user_role / role_permission 的 role_id 外键是 ON DELETE CASCADE,删角色会自动解绑
    db.delete(role)
    return success_response()


@role_router.post(
    "/assign/permission", summary="给角色分配权限", description="分配权限"
)
def assign_permission(payload: AssignPermissionRequest, db: Session = Depends(get_db)):
    # 获取角色
    role = db.get(Role, payload.roleId)
    if not role:
        raise BusinessError(code=Code.ROLE_NOT_EXIST, message="角色不存在")
    # 没有权限
    all_permission_ids = db.scalars(select(Permission.id)).all()

    if any(
        permission_id not in all_permission_ids
        for permission_id in payload.permissionId
    ):
        raise BusinessError(code=Code.PARAM_ERROR, message="权限不存在")
    # 先删除再分配
    db.execute(delete(RolePermission).where(RolePermission.role_id == payload.roleId))
    db.execute(
        insert(RolePermission).values(
            [
                {"role_id": payload.roleId, "permission_id": permission_id}
                for permission_id in payload.permissionId
            ]
        )
    )
    return success_response(message="成功")


@role_router.get("/getAllPermissions/{roleId}", summary="角色拥有哪些权限")
def get_all_role_permissions(
    roleId: int, request: Request, db: Session = Depends(get_db)
):
    # 获取角色
    role = db.get(Role, roleId)
    if not role:
        raise BusinessError(code=Code.ROLE_NOT_EXIST, message="角色不存在")

    # 返回树状列表并且添加check属性:角色已拥有的权限 check=1,否则 0
    tree = get_tree_menu(db, roleId)
    return success_response(data=tree)


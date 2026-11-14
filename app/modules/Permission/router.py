from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
import rich
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.modules.Permission.database import Permission
from app.modules.Permission.schemas import (
    CreateMenuRequest,
    CreateMenuResponse,
    MenuTreeResponse,
    UpdateMenuRequest,
)
from app.common.base_response import success_response
from app.common.business_error import BusinessError
from app.common.error_code import Code
from app.database import get_db
from app.modules.Permission.services import get_tree_menu

api_bearer = HTTPBearer()
menu_router = APIRouter(
    prefix="/menu", tags=["菜单管理"], dependencies=[Depends(api_bearer)]
)


# 创建菜单
@menu_router.post("/create", description="创建菜单", summary="创建菜单")
def create_menu(create_menu_dto: CreateMenuRequest, db: Session = Depends(get_db)):
    menu = db.scalars(
        select(Permission).where(
            or_(
                Permission.code == create_menu_dto.code,
                Permission.name == create_menu_dto.name,
            )
        )
    ).all()
    if menu:
        raise BusinessError(message="菜单已存在", http_status=Code.PARAM_ERROR)

    new_menu = Permission(**create_menu_dto.model_dump())
    db.add(new_menu)
    return success_response()


# 获取平铺菜单列表
@menu_router.get("/list", description="获取平铺菜单列表", summary="获取平铺菜单列表")
def get_menu_list(db: Session = Depends(get_db)):
    stmt = select(Permission).where(Permission.status == 1)
    menu_list = db.scalars(stmt).all()
    return success_response(
        data=[CreateMenuResponse.model_validate(menu) for menu in list(menu_list)]
    )


#
@menu_router.put("/update", description="更新菜单", summary="更新菜单")
def update_menu(payload: UpdateMenuRequest, db: Session = Depends(get_db)):
    menu = db.get(Permission, payload.id)
    if menu is None:
        raise BusinessError(message="菜单不存在")
    for key, value in payload.model_dump().items():
        setattr(menu, key, value)

    return success_response()


#
@menu_router.get("/tree", summary="获取菜单树", description="获取菜单树")
def get_menu_tree(db: Session = Depends(get_db)):
    tree = get_tree_menu(db)

    return success_response(data=tree)


@menu_router.delete("/delete/{menu_id}", description="删除菜单", summary="删除菜单")
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    menu = db.scalar(select(Permission).where(Permission.id == menu_id))
    if menu is None:
        raise BusinessError(code=Code.MENU_NOT_EXIST, message="菜单不存在")
    child = db.scalar(select(Permission).where(Permission.pid == menu_id))
    if child is not None:
        raise BusinessError(code=Code.MENU_NOT_EMPTY, message="菜单下有子菜单")
    db.delete(menu)
    return success_response(message="删除成功")

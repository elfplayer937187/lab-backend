from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi.security import HTTPBearer
import rich
from sqlalchemy import and_, or_, select, func
from sqlalchemy.orm import Session

from app.modules.User.database import User
from app.common.base_response import pagination_response, success_response
from app.common.business_error import BusinessError
from app.common.error_code import Code
from app.database import get_db
from app.modules.lab.database import Lab
from app.modules.lab.schemas import (
    CreateLabRequest,
    GetLabListRequest,
    GetLabListResponse,
    GetUserListResponse,
    UpdateLabRequest,
)

bearer = HTTPBearer()
lab_router = APIRouter(
    prefix="/lab", tags=["实验室管理"], dependencies=[Depends(bearer)]
)


@lab_router.post("/create", summary="创建实验室", description="创建实验室")
def create_lab(create_lab_dto: CreateLabRequest, db: Session = Depends(get_db)):
    lab = db.scalar(select(Lab).where(Lab.name == create_lab_dto.name))
    if lab:
        raise BusinessError(
            code=Code.LAB_EXIST, message="实验室存在", http_status=Code.LAB_EXIST
        )
    db.add(Lab(**create_lab_dto.model_dump()))
    return success_response().model_dump()


@lab_router.get("/list", summary="获取实验室列表", description="获取实验室列表")
def get_lab_list(
    payload: Annotated[GetLabListRequest, Query()], db: Session = Depends(get_db)
):
    conditions = []
    # 拼接字符串防止注入
    if payload.nameKeyword:
        like = f"%{payload.nameKeyword}%"
        conditions.append(
            and_(
                Lab.name.like(like),
            )
        )
    # 三个新字段为精确匹配,不传(None)则不参与筛选
    if payload.building is not None:
        conditions.append(Lab.building == payload.building)
    if payload.floor is not None:
        conditions.append(Lab.floor == payload.floor)
    if payload.manage_id is not None:
        conditions.append(Lab.manager_id == payload.manage_id)
    total = db.scalar(select(func.count()).select_from(Lab).where(*conditions))
    stmt = (
        select(Lab)
        .where(*conditions)
        .limit(payload.pageSize)
        .offset((payload.page - 1) * payload.pageSize)
        .order_by(Lab.id.asc())
    )
    labs = db.execute(stmt).scalars().all()
    return success_response(
        data=pagination_response(
            total=total or 0,
            page=payload.page,
            page_size=payload.pageSize,
            records=[GetLabListResponse.model_validate(lab) for lab in labs],
        ),
        message="成功",
    )


@lab_router.put("/update", summary="更新实验室", description="更新实验室")
def update_lab(payload: UpdateLabRequest, db: Session = Depends(get_db)):
    lab = db.get(Lab, payload.id)
    if lab is None:
        raise BusinessError(
            code=Code.LAB_NOT_EXIST,
            message="实验室不存在",
            http_status=Code.LAB_NOT_EXIST,
        )
    update_data = payload.model_dump(
        exclude_unset=True, exclude={"id"}, exclude_none=True
    )
    for key, value in update_data.items():
        setattr(lab, key, value)

    return success_response()


@lab_router.delete("/delete/{labId}", summary="删除实验室", description="删除实验室")
def delete_lab(labId: int, db: Session = Depends(get_db)):
    lab = db.get(Lab, labId)
    if lab is None:
        raise BusinessError(
            code=Code.LAB_NOT_EXIST,
            message="实验室不存在",
            http_status=Code.LAB_NOT_EXIST,
        )
    db.delete(lab)
    return success_response()


@lab_router.get("/get/{labId}", summary="获取实验室详情", description="获取实验室详情")
def get_lab_detail(labId: int, db: Session = Depends(get_db)):
    lab = db.get(Lab, labId)
    if lab is None:
        raise BusinessError(
            code=Code.LAB_NOT_EXIST,
            message="实验室不存在",
            http_status=Code.LAB_NOT_EXIST,
        )
    return success_response(data=GetLabListResponse.model_validate(lab))


@lab_router.get("/all/manager", summary="获取管理员列表", description="获取管理员列表")
def get_manager_id(db: Session = Depends(get_db)):
    users = (
        db.execute(select(User.id, User.username).where(User.status == 1)).all()
    )
    rich.print(users)
    return success_response(
        data=[GetUserListResponse.model_validate(user) for user in users]
    )

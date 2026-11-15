from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi.security import HTTPBearer
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.common.base_response import pagination_response, success_response
from app.common.business_error import BusinessError
from app.common.error_code import Code
from app.database import get_db
from app.modules.lab.lab_device.database import LabDevice
from app.modules.lab.lab_device_type.database import LabDeviceType
from app.modules.lab.lab_device_type.schemas import (
    CreateDeviceTypeRequest,
    GetDeviceTypeListRequest,
    GetDeviceTypeResponse,
    UpdateDeviceTypeRequest,
    UpdateDeviceTypeStatusRequest,
)

device_type_router = APIRouter(
    prefix="/lab_device_type",
    tags=["实验室设备类型管理"],
    dependencies=[Depends(HTTPBearer())],
)


@device_type_router.post("/create", summary="创建设备类型", description="创建设备类型")
def create_device_type(
    payload: CreateDeviceTypeRequest, db: Session = Depends(get_db)
):
    # type_name / type_code 都是唯一列,先查一次给友好提示,而不是等 DB 抛 IntegrityError
    exists = db.scalar(
        select(LabDeviceType).where(
            or_(
                LabDeviceType.type_name == payload.type_name,
                LabDeviceType.type_code == payload.type_code,
            )
        )
    )
    if exists:
        raise BusinessError(
            code=Code.DEVICE_TYPE_EXIST, message="设备类型已存在"
        )
    db.add(LabDeviceType(**payload.model_dump()))
    return success_response()


@device_type_router.get("/list", summary="分页查询设备类型", description="分页查询设备类型")
def get_device_type_list(
    payload: Annotated[GetDeviceTypeListRequest, Query()],
    db: Session = Depends(get_db),
):
    conditions = []
    # like 的参数由 SQLAlchemy 绑定,不做字符串拼 SQL
    if payload.keyword:
        like = f"%{payload.keyword}%"
        conditions.append(
            or_(
                LabDeviceType.type_name.like(like),
                LabDeviceType.type_code.like(like),
            )
        )
    if payload.status is not None:
        conditions.append(LabDeviceType.status == payload.status)

    total = db.scalar(
        select(func.count()).select_from(LabDeviceType).where(*conditions)
    )
    stmt = (
        select(LabDeviceType)
        .where(*conditions)
        # 显式排序,否则 MySQL 不保证顺序,翻页会重复或漏记录
        .order_by(LabDeviceType.type_id.asc())
        .offset((payload.page - 1) * payload.pageSize)
        .limit(payload.pageSize)
    )
    types = db.execute(stmt).scalars().all()
    return success_response(
        data=pagination_response(
            total=total or 0,
            page=payload.page,
            page_size=payload.pageSize,
            records=[GetDeviceTypeResponse.model_validate(t) for t in types],
        )
    )


@device_type_router.get(
    "/get/{typeId}", summary="获取设备类型详情", description="获取设备类型详情"
)
def get_device_type_detail(typeId: int, db: Session = Depends(get_db)):
    device_type = db.get(LabDeviceType, typeId)
    if device_type is None:
        raise BusinessError(
            code=Code.DEVICE_TYPE_NOT_EXIST, message="设备类型不存在"
        )
    return success_response(data=GetDeviceTypeResponse.model_validate(device_type))


@device_type_router.put("/update", summary="更新设备类型", description="更新设备类型")
def update_device_type(
    payload: UpdateDeviceTypeRequest, db: Session = Depends(get_db)
):
    device_type = db.get(LabDeviceType, payload.type_id)
    if device_type is None:
        raise BusinessError(
            code=Code.DEVICE_TYPE_NOT_EXIST, message="设备类型不存在"
        )
    # 唯一性检查要排除自己,否则不改 name/code 直接提交也会被自己挡住
    exists = db.scalar(
        select(LabDeviceType).where(
            LabDeviceType.type_id != payload.type_id,
            or_(
                LabDeviceType.type_name == payload.type_name,
                LabDeviceType.type_code == payload.type_code,
            ),
        )
    )
    if exists:
        raise BusinessError(
            code=Code.DEVICE_TYPE_EXIST, message="设备类型已存在"
        )
    for key, value in payload.model_dump(exclude={"type_id"}).items():
        setattr(device_type, key, value)
    return success_response()


@device_type_router.put(
    "/updateStatus", summary="启用或禁用设备类型", description="启用或禁用设备类型"
)
def update_device_type_status(
    payload: UpdateDeviceTypeStatusRequest, db: Session = Depends(get_db)
):
    device_type = db.get(LabDeviceType, payload.type_id)
    if device_type is None:
        raise BusinessError(
            code=Code.DEVICE_TYPE_NOT_EXIST, message="设备类型不存在"
        )
    device_type.status = payload.status
    return success_response()


@device_type_router.delete(
    "/delete/{typeId}", summary="删除设备类型", description="删除设备类型"
)
def delete_device_type(typeId: int, db: Session = Depends(get_db)):
    device_type = db.get(LabDeviceType, typeId)
    if device_type is None:
        raise BusinessError(
            code=Code.DEVICE_TYPE_NOT_EXIST, message="设备类型不存在"
        )
    # 先自己查一遍引用:外键约束要到 commit 时才报 IntegrityError,
    # 那时只能兜成 500 系统错误,前端看不出原因。
    if db.scalar(select(LabDevice).where(LabDevice.type_id == typeId)):
        raise BusinessError(
            code=Code.DEVICE_TYPE_IN_USE, message="该类型下还有设备,不能删除"
        )
    db.delete(device_type)
    return success_response()

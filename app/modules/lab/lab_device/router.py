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
from app.modules.lab.lab_device.schemas import (
    CreateLabDeviceRequest,
    GetLabDeviceListRequest,
    GetLabDeviceResponse,
    UpdateLabDeviceRequest,
    UpdateLabDeviceStatusRequest,
)
from app.modules.lab.lab_device_stock.database import LabDeviceStock
from app.modules.lab.lab_device_type.database import LabDeviceType

lab_device_router = APIRouter(
    prefix="/lab_device",
    tags=["实验室设备资料管理"],
    dependencies=[Depends(HTTPBearer())],
)


def _check_type_exists(type_id: int, db: Session) -> None:
    # 类型 id 有外键约束,不先查一次的话非法 id 要到 commit 才报 IntegrityError(500)
    if db.get(LabDeviceType, type_id) is None:
        raise BusinessError(
            code=Code.DEVICE_TYPE_NOT_EXIST, message="设备类型不存在"
        )


@lab_device_router.post("/create", summary="创建设备资料", description="创建设备资料")
def create_lab_device(
    payload: CreateLabDeviceRequest, db: Session = Depends(get_db)
):
    # device_code 是唯一列,先查一次给友好提示,而不是等 DB 抛 IntegrityError
    if db.scalar(
        select(LabDevice).where(LabDevice.device_code == payload.device_code)
    ):
        raise BusinessError(code=Code.DEVICE_EXIST, message="设备编号已存在")
    _check_type_exists(payload.type_id, db)
    db.add(LabDevice(**payload.model_dump()))
    return success_response()


@lab_device_router.get("/list", summary="分页查询设备资料", description="分页查询设备资料")
def get_lab_device_list(
    payload: Annotated[GetLabDeviceListRequest, Query()],
    db: Session = Depends(get_db),
):
    conditions = []
    # like 的参数由 SQLAlchemy 绑定,不做字符串拼 SQL
    if payload.keyword:
        like = f"%{payload.keyword}%"
        conditions.append(
            or_(
                LabDevice.device_name.like(like),
                LabDevice.device_code.like(like),
            )
        )
    if payload.type_id is not None:
        conditions.append(LabDevice.type_id == payload.type_id)
    if payload.status is not None:
        conditions.append(LabDevice.status == payload.status)

    total = db.scalar(select(func.count()).select_from(LabDevice).where(*conditions))
    stmt = (
        select(LabDevice)
        .where(*conditions)
        # 显式排序,否则 MySQL 不保证顺序,翻页会重复或漏记录
        .order_by(LabDevice.lab_device_id.asc())
        .offset((payload.page - 1) * payload.pageSize)
        .limit(payload.pageSize)
    )
    devices = db.execute(stmt).scalars().all()
    return success_response(
        data=pagination_response(
            total=total or 0,
            page=payload.page,
            page_size=payload.pageSize,
            records=[GetLabDeviceResponse.model_validate(d) for d in devices],
        )
    )


@lab_device_router.get(
    "/get/{deviceId}", summary="获取设备资料详情", description="获取设备资料详情"
)
def get_lab_device_detail(deviceId: int, db: Session = Depends(get_db)):
    device = db.get(LabDevice, deviceId)
    if device is None:
        raise BusinessError(code=Code.DEVICE_NOT_EXIST, message="设备不存在")
    return success_response(data=GetLabDeviceResponse.model_validate(device))


@lab_device_router.put("/update", summary="更新设备资料", description="更新设备资料")
def update_lab_device(payload: UpdateLabDeviceRequest, db: Session = Depends(get_db)):
    device = db.get(LabDevice, payload.lab_device_id)
    if device is None:
        raise BusinessError(code=Code.DEVICE_NOT_EXIST, message="设备不存在")
    # 唯一性检查要排除自己,否则不改编号直接提交也会被自己挡住
    if db.scalar(
        select(LabDevice).where(
            LabDevice.device_code == payload.device_code,
            LabDevice.lab_device_id != payload.lab_device_id,
        )
    ):
        raise BusinessError(code=Code.DEVICE_EXIST, message="设备编号已存在")
    _check_type_exists(payload.type_id, db)
    for key, value in payload.model_dump(exclude={"lab_device_id"}).items():
        setattr(device, key, value)
    return success_response()


@lab_device_router.put(
    "/updateStatus", summary="启用或禁用设备", description="启用或禁用设备"
)
def update_lab_device_status(
    payload: UpdateLabDeviceStatusRequest, db: Session = Depends(get_db)
):
    device = db.get(LabDevice, payload.lab_device_id)
    if device is None:
        raise BusinessError(code=Code.DEVICE_NOT_EXIST, message="设备不存在")
    device.status = payload.status
    return success_response()


@lab_device_router.delete("/delete/{deviceId}", summary="删除设备", description="删除设备")
def delete_lab_device(deviceId: int, db: Session = Depends(get_db)):
    device = db.get(LabDevice, deviceId)
    if device is None:
        raise BusinessError(code=Code.DEVICE_NOT_EXIST, message="设备不存在")
    # 设备被库存(lab_device_stock)引用时外键会拦,提前查一次换成业务错误
    if db.scalar(
        select(LabDeviceStock).where(LabDeviceStock.device_id == deviceId)
    ):
        raise BusinessError(code=Code.DEVICE_IN_USE, message="设备已被实验室使用,不能删除")
    db.delete(device)
    return success_response()

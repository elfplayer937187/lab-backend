from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi.security import HTTPBearer
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.common.base_response import pagination_response, success_response
from app.common.business_error import BusinessError
from app.common.error_code import Code
from app.database import get_db
from app.modules.lab.database import Lab
from app.modules.lab.lab_device.database import LabDevice
from app.modules.lab.lab_device_stock.database import LabDeviceStock
from app.modules.lab.lab_device_stock.schemas import (
    CreateLabDeviceStockRequest,
    GetLabDeviceStockListRequest,
    LabDeviceStockResponse,
    UpdateLabDeviceStockRequest,
)
from app.modules.lab.lab_device_type.database import LabDeviceType

stock_router = APIRouter(
    prefix="/lab_device_stock",
    tags=["实验室设备管理"],
    dependencies=[Depends(HTTPBearer())],
)


def _build_response(
    stock: LabDeviceStock, device: LabDevice, type_name: str
) -> LabDeviceStockResponse:
    return LabDeviceStockResponse(
        id=stock.id,
        lab_id=stock.lab_id,
        device_id=stock.device_id,
        quantity=stock.quantity,
        available_quantity=stock.available_quantity,
        location=stock.location,
        remark=stock.remark,
        device_name=device.device_name,
        device_code=device.device_code,
        brand=device.brand,
        type_id=device.type_id,
        type_name=type_name,
        device_status=device.status,
    )


@stock_router.post("/create", summary="给实验室添加设备", description="给实验室添加设备")
def create_lab_device_stock(
    payload: CreateLabDeviceStockRequest, db: Session = Depends(get_db)
):
    if db.get(Lab, payload.lab_id) is None:
        raise BusinessError(code=Code.LAB_NOT_EXIST, message="实验室不存在")
    if db.get(LabDevice, payload.device_id) is None:
        raise BusinessError(code=Code.DEVICE_NOT_EXIST, message="设备不存在")
    # 同一实验室同一设备只允许一条记录,数量改这条记录即可
    if db.scalar(
        select(LabDeviceStock).where(
            LabDeviceStock.lab_id == payload.lab_id,
            LabDeviceStock.device_id == payload.device_id,
        )
    ):
        raise BusinessError(code=Code.STOCK_EXIST, message="该实验室已添加过此设备")
    # 刚添加时还没被借出,可用数量 = 总数量
    db.add(
        LabDeviceStock(**payload.model_dump(), available_quantity=payload.quantity)
    )
    return success_response()


@stock_router.get("/list", summary="查询实验室设备列表", description="查询实验室设备列表")
def get_lab_device_stock_list(
    payload: Annotated[GetLabDeviceStockListRequest, Query()],
    db: Session = Depends(get_db),
):
    conditions = [LabDeviceStock.lab_id == payload.lab_id]
    # like 的参数由 SQLAlchemy 绑定,不做字符串拼 SQL
    if payload.keyword:
        like = f"%{payload.keyword}%"
        conditions.append(
            or_(
                LabDevice.device_name.like(like),
                LabDevice.device_code.like(like),
                LabDevice.brand.like(like),
            )
        )
    if payload.type_id is not None:
        conditions.append(LabDevice.type_id == payload.type_id)

    total = db.scalar(
        select(func.count())
        .select_from(LabDeviceStock)
        .join(LabDevice, LabDevice.lab_device_id == LabDeviceStock.device_id)
        .join(LabDeviceType, LabDeviceType.type_id == LabDevice.type_id)
        .where(*conditions)
    )
    stmt = (
        select(LabDeviceStock, LabDevice, LabDeviceType.type_name)
        .join(LabDevice, LabDevice.lab_device_id == LabDeviceStock.device_id)
        .join(LabDeviceType, LabDeviceType.type_id == LabDevice.type_id)
        .where(*conditions)
        # 显式排序,否则 MySQL 不保证顺序,翻页会重复或漏记录
        .order_by(LabDeviceStock.id.asc())
        .offset((payload.page - 1) * payload.pageSize)
        .limit(payload.pageSize)
    )
    rows = db.execute(stmt).all()
    return success_response(
        data=pagination_response(
            total=total or 0,
            page=payload.page,
            page_size=payload.pageSize,
            records=[
                _build_response(stock, device, type_name)
                for stock, device, type_name in rows
            ],
        )
    )


@stock_router.get(
    "/get/{stockId}", summary="获取实验室设备详情", description="获取实验室设备详情"
)
def get_lab_device_stock_detail(stockId: int, db: Session = Depends(get_db)):
    stock = db.get(LabDeviceStock, stockId)
    if stock is None:
        raise BusinessError(code=Code.STOCK_NOT_EXIST, message="设备记录不存在")
    device = db.get(LabDevice, stock.device_id)
    if device is None:
        raise BusinessError(code=Code.DEVICE_NOT_EXIST, message="设备不存在")
    device_type = db.get(LabDeviceType, device.type_id)
    return success_response(
        data=_build_response(
            stock, device, device_type.type_name if device_type else ""
        )
    )


@stock_router.put("/update", summary="修改实验室设备", description="修改实验室设备")
def update_lab_device_stock(
    payload: UpdateLabDeviceStockRequest, db: Session = Depends(get_db)
):
    stock = db.get(LabDeviceStock, payload.id)
    if stock is None:
        raise BusinessError(code=Code.STOCK_NOT_EXIST, message="设备记录不存在")

    # 只写显式传上来的字段;清空 location / remark 传空字符串,不要传 null
    data = payload.model_dump(
        exclude_unset=True, exclude_none=True, exclude={"id"}
    )
    quantity = data.get("quantity", stock.quantity)

    # 只改数量时,可用数量跟着数量同幅变化(已借出的数量保持不变);
    # 显式传了 available_quantity 就以传入值为准。
    if "quantity" in data and "available_quantity" not in data:
        available = stock.available_quantity + (data["quantity"] - stock.quantity)
        if available < 0:
            raise BusinessError(
                code=Code.PARAM_ERROR, message="可用数量不足,不能减少到该数量"
            )
        data["available_quantity"] = available
    if data.get("available_quantity", stock.available_quantity) > quantity:
        raise BusinessError(
            code=Code.PARAM_ERROR, message="可用数量不能大于设备数量"
        )

    for key, value in data.items():
        setattr(stock, key, value)
    return success_response()


@stock_router.delete(
    "/delete/{stockId}", summary="删除实验室设备", description="删除实验室设备"
)
def delete_lab_device_stock(stockId: int, db: Session = Depends(get_db)):
    stock = db.get(LabDeviceStock, stockId)
    if stock is None:
        raise BusinessError(code=Code.STOCK_NOT_EXIST, message="设备记录不存在")
    db.delete(stock)
    return success_response()

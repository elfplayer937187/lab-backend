from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBearer
from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from app.common.base_response import pagination_response, success_response
from app.common.business_error import BusinessError
from app.common.error_code import Code
from app.database import get_db
from app.modules.lab.database import Lab
from app.modules.lab_book.database import LabBook
from app.modules.lab_book.schemas import (
    AcceptPayload,
    CreateLabBookRequest,
    LabBookListResponse,
    LabBookListWaitAcceptResponse,
)
from app.modules.lab_book.service import is_conflict
from app.modules.User.database import User

lab_book_router = APIRouter(
    prefix="/lab_book", tags=["实验室预约管理"], dependencies=[Depends(HTTPBearer())]
)


@lab_book_router.post("/create", summary="创建实验室预约", description="创建实验室预约")
def create_lab_book(
    request: Request,
    create_lab_book_dto: CreateLabBookRequest,
    db: Session = Depends(get_db),
):
    if create_lab_book_dto.end_time <= create_lab_book_dto.start_time:
        raise BusinessError(code=Code.PARAM_ERROR, message="结束时间必须大于开始时间")
    lab = db.get(Lab, create_lab_book_dto.lab_id)
    if not lab:
        raise BusinessError(
            code=Code.LAB_NOT_EXIST,
            message="实验室不存在",
            http_status=Code.LAB_NOT_EXIST,
        )
    user_id = request.state.user_id
    if is_conflict(
        lab.id,
        create_lab_book_dto.start_time,
        create_lab_book_dto.end_time,
        create_lab_book_dto.people_count,
        db=db,
    ):
        raise BusinessError(
            code=Code.LAB_BOOK_CONFLICT,
            message="实验室冲突",
            http_status=Code.LAB_BOOK_CONFLICT,
        )
    # 是否能够预定
    # 1.实验室开放时间
    # 2.实验室预约人数<容量
    # 3.是否冲突
    db.add(
        LabBook(
            user_id=user_id,
            lab_id=create_lab_book_dto.lab_id,
            start_time=create_lab_book_dto.start_time,
            end_time=create_lab_book_dto.end_time,
            people_count=create_lab_book_dto.people_count,
            status=0,
        )
    )
    return success_response(message="预约成功")


# 所有预约记录表等待审批
@lab_book_router.get(
    "/list/accept",
    summary="获取所有预约记录表等待审批",
    description="获取所有预约记录表等待审批",
)
def get_lab_book_list_wait_accept(
    request: Request, page: int, limit: int, db: Session = Depends(get_db)
):

    user_id = request.state.user_id
    # total / 待审核 / 已通过 一次聚合查出来,省掉另外两次 COUNT,三个数也来自同一快照
    total, wait_accept, accept = db.execute(
        select(
            func.count(LabBook.id).label('total'),
            func.count(case((LabBook.status == 0, 1))).label('wait_accept'),
            func.count(case((LabBook.status == 1, 1))).label('accept'),
        ).where(LabBook.reviewer_id == user_id)
    ).one()
    stmt = (
        select(
            *LabBook.__table__.columns,
            User.name.label("username"),
            Lab.image.label("image"),
            Lab.name.label("lab_name"),
        )
        .join(User, LabBook.user_id == User.id)
        .join(Lab, LabBook.lab_id == Lab.id)
        .where(LabBook.reviewer_id == user_id)
        .limit(limit)
        .offset((page - 1) * limit)
        .order_by(LabBook.status.desc(), LabBook.id.desc())
    )
    data = db.execute(stmt).mappings().all()
    return success_response(
        data={
            "records": [
                LabBookListWaitAcceptResponse.model_validate(lab_book)
                for lab_book in data
            ],
            "total": total or 0,
            "page": page,
            "page_size": limit,
            "wait_accept": wait_accept or 0,
            "accept": accept or 0,
        },
    )


@lab_book_router.get(
    "/list/{id}", summary="获取当前实验室预约详情列表", description="获取预约列表"
)
def get_lab_book_list(id: int, db: Session = Depends(get_db)):
    lab_book_list = (
        db.execute(
            select(*LabBook.__table__.columns, User.name.label("username"))
            .join(User, LabBook.user_id == User.id)
            .where(LabBook.lab_id == id)
        )
        .mappings()
        .all()
    )
    return success_response(
        data=[
            LabBookListResponse.model_validate(lab_book) for lab_book in lab_book_list
        ]
    )


@lab_book_router.post("/accept", summary="审批预约", description="审批预约")
def accept_lab_book(
    request: Request, accept_payload: AcceptPayload, db: Session = Depends(get_db)
):
    user_id = request.state.user_id
    lab_book = db.get(LabBook, accept_payload.LabBookId)
    if lab_book is None or lab_book.reviewer_id != user_id:
        raise BusinessError(
            code=Code.LAB_BOOK_NOT_EXIST,
            message="预约不存在",
            http_status=Code.LAB_BOOK_NOT_EXIST,
        )

    lab_book.status = accept_payload.status
    lab_book.reviewer_remark = accept_payload.remark
    lab_book.reviewer_id = user_id

    return success_response(message="审批成功")

from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.common.base_response import success_response
from app.common.business_error import BusinessError
from app.common.error_code import Code
from app.database import get_db
from app.modules.User.database import User
from app.modules.lab.database import Lab
from app.modules.lab_book.database import LabBook
from app.modules.lab_book.schemas import CreateLabBookRequest, LabBookListResponse
from app.modules.lab_book.service import is_conflict

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


@lab_book_router.get(
    "/list/{id}", summary="获取当前实验室预约列表", description="获取预约列表"
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




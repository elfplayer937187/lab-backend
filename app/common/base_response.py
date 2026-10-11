from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

from app.common.error_code import Code

T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):
    code: int = 200
    message: Optional[str] = None
    data: Optional[T] = None


class PaginationResponse(BaseModel, Generic[T]):

    records: Optional[T] = None
    total: int = 0
    page: int = 1
    pageSize: int = 10


def success_response(
    data: Optional[T] = None, message: Optional[str] = None
) -> BaseResponse:
    return BaseResponse(code=200, message=message, data=data)


def error_response(
    code: int = Code.SYSTEM_ERROR,
    message: Optional[str] = "系统错误",
    data: Optional[T] = None,
) -> BaseResponse:
    return BaseResponse(code=code, message=message, data=data)


def pagination_response(
    records: Optional[T] = None, total: int = 0, page: int = 1, page_size: int = 10
):
    return PaginationResponse(
        records=records, total=total, page=page, pageSize=page_size
    )

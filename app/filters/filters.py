# 定义全局异常处理
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.common.base_response import error_response
from app.common.business_error import BusinessError
from app.common.error_code import HTTP_STATUS, Code


# 处理参数错误，平铺错误
def _flatten_errors(exc: RequestValidationError) -> list[str]:
    """把 pydantic 的嵌套错误压平成 'body.username: Field required' 这样的字符串列表"""
    details: list[str] = []
    for error in exc.errors():
        loc = '.'.join(str(part) for part in error.get('loc', ()))
        msg = error.get('msg') or ''
        details.append(f'{loc}: {msg}' if loc else msg)
    return details


async def BusinessErrorHandler(request: Request, exc: BusinessError) -> JSONResponse:
    # HTTP 状态码取 exc.http_status(抛异常时指定,或按 HTTP_STATUS 表兜底),
    # body.code 才是业务码 —— 两者不再混为一谈
    return JSONResponse(
        status_code=exc.http_status,
        content=error_response(exc.code, exc.message, exc.data).model_dump(),
    )


async def RequestValidationErrorHandler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=HTTP_STATUS[Code.PARAM_ERROR],
        content=error_response(Code.PARAM_ERROR, '参数错误', _flatten_errors(exc)).model_dump(),
    )


# 兜底filter
async def UnhandledErrorHandler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=HTTP_STATUS[Code.SYSTEM_ERROR],
        content=error_response(Code.SYSTEM_ERROR, '系统错误').model_dump(),
    )

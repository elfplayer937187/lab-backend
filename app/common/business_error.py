from typing import Any

from app.common.error_code import HTTP_STATUS, Code


# 通用业务异常
class BusinessError(Exception):
    def __init__(
        self,
        code: int = Code.UNKNOWN_ERROR,
        message: str = '未知错误',
        data: Any = None,
        http_status: int | None = None,
    ):
        self.code = code
        self.message = message
        self.data = data
        # HTTP 状态码和业务码是两回事:业务码给前端判分支用,HTTP 状态码给访问日志、
        # 业务异常基本都属于「这次请求不被接受」。

        # http_status 按这个顺序决定,取到就停:
        #   1. 抛异常时显式传的 http_status(优先级最高,用于同一业务码在不同接口语义不同的场景)
        #   2. HTTP_STATUS[code] 兜底映射表
        #   3. 字面量 400 —— 业务异常基本都是「请求不被接受」
        # 注意 Code 不参与这个推导,它只是业务码常量,和 HTTP 状态码无关。
        self.http_status = http_status if http_status is not None else HTTP_STATUS.get(code, 400)

        super().__init__(self.message)

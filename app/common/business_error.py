from typing import Any

from app.common.error_code import Code


# 通用业务异常
class BusinessError(Exception):
    def __init__(self, code: int = Code.UNKNOWN_ERROR, message: str = '未知错误', data: Any = None):
        self.code = code
        self.message = message
        self.data = data

        super().__init__(self.message)

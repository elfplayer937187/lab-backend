from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.common.base_response import error_response
from app.common.business_error import BusinessError
from app.utils.jwt import get_token_from_request, verify_access_token

# 免鉴权路径。request.url.path 永远以 / 开头,所以这里必须写完整的绝对路径,
# 空字符串或漏掉开头斜杠的写法永远匹配不上。
WHITE_LIST = frozenset(
    {
        "/api/auth/login",  # 登录本身不能要求 token,否则没有 token 就换不到 token
        "/api/auth/register",
        "/docs",
        "/docs/oauth2-redirect",
        "/openapi.json",  # /docs 页面靠它拿接口定义,不放行则文档列表是空的
        "/redoc",
        "/uploads/*",
    }
)


class JWTMiddleWare(BaseHTTPMiddleware):
    """
    JWT 认证中间件

    职责：
    1. 检查请求路径是否在公开列表中，是则放行
    2. 从 header 提取 token
    3. 验证 token 有效性
    4. 将用户信息存入 request.state 供后续使用
    5. token 无效则返回 401
    """

    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/uploads"):
            return await call_next(request)
        print(request.url.path)
        if request.url.path in WHITE_LIST:
            return await call_next(request)
        try:
            token = get_token_from_request(request)
        except BusinessError as e:
            return JSONResponse(
                status_code=e.http_status,
                content=error_response(e.code, e.message, e.data).model_dump(),
            )
        try:
            payload = verify_access_token(token)
        except BusinessError as e:
            return JSONResponse(
                status_code=e.http_status,
                content=error_response(e.code, e.message, e.data).model_dump(),
            )

        request.state.username = payload["username"]
        request.state.user_id = payload["userId"]

        return await call_next(request)

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.utils.jwt import get_token_from_request, verify_access_token

WhiteList = [
    '',
    '',
]


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
        if request.url.path in WhiteList:
            return await call_next(request)
        token = get_token_from_request(request)
        payload = verify_access_token(token)

        request.state.username = payload['username']
        request.state.role = payload['role']
        request.state.user_id = payload['userId']

        return await call_next(request)

from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Request

from app.common.business_error import BusinessError
from app.common.error_code import Code
from app.config import settings

ISSUE_ALGORITHM = 'HS256'
ISSUER = 'AILAB'


# 创建token
def create_access_token(user_id: int, username: str, role: str) -> str:
    now = datetime.now(tz=timezone.utc)
    expire_time = now + timedelta(hours=settings.JWT_EXPIRATION_HOURS)
    payload = {
        'username': username,
        'userId': user_id,
        'role': role,
        'exp': expire_time,
        'iat': now,
        'iss': ISSUER,
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=ISSUE_ALGORITHM)


# 解码token
def decode_access_token(token: str) -> dict:
    payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[ISSUE_ALGORITHM])
    return payload


# 验证token
def verify_access_token(token: str) -> dict:
    payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[ISSUE_ALGORITHM])
    if payload.get('iss') != ISSUER:
        raise BusinessError(code=Code.TOKEN_INVALID, message='无效的token')
    return payload


# 从请求投提取token内容
def get_token_from_request(request: Request) -> dict:
    token = request.headers.get('token')
    if not token:
        raise BusinessError(code=Code.TOKEN_INVALID, message='未找到token')
    try:
        payload = verify_access_token(token)
        return payload
    except jwt.exceptions.DecodeError:
        raise BusinessError(code=Code.TOKEN_INVALID, message='无效的token')

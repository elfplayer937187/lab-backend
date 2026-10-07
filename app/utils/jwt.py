from datetime import datetime, timedelta, timezone
from typing import TypedDict, cast

import jwt
from fastapi import Request

from app.common.business_error import BusinessError
from app.common.error_code import Code
from app.config import settings

ISSUE_ALGORITHM = 'HS256'
ISSUER = 'AILAB'


class TokenPayload(TypedDict):
    """JWT 载荷。

    键名就是 token 里的字段名,改名等于让所有已签发的 token 全部失效(旧 token 解出来
    还是老键名),所以这个名字要当成对外契约看,不要随手改。

    exp / iat 写成 datetime | int,是因为同一个载荷在签发和解码两侧形态不同:
    - 签发:`create_access_token` 传的是 datetime,由 PyJWT 负责转成时间戳
    - 解码:`jwt.decode` 返回的是已经转好的 Unix 时间戳(int)

    两者都在这个类型里,是为了不为两侧各维护一个几乎一样的 TypedDict。
    """

    username: str
    userId: int
    role: str
    iss: str
    exp: datetime | int
    iat: datetime | int


# 创建token
def create_access_token(user_id: int, username: str, role: str) -> str:
    now = datetime.now(tz=timezone.utc)
    expire_time = now + timedelta(hours=settings.JWT_EXPIRATION_HOURS)
    payload: TokenPayload = {
        'username': username,
        'userId': user_id,
        'role': role,
        'exp': expire_time,
        'iat': now,
        'iss': ISSUER,
    }
    # dict(payload) 看着多余,但绕不开:PyJWT 的 encode 签名写的是 dict[str, Any],
    # 而 TypedDict 不是 dict 的子类型(它是「具有这些键的 Mapping」,不保证没有别的键),
    # 直接传会报类型错。转一次拿到真 dict,顺带避免 encode 改动我们这份。
    return jwt.encode(dict(payload), settings.JWT_SECRET_KEY, algorithm=ISSUE_ALGORITHM)


# 解码token
def decode_access_token(token: str) -> TokenPayload:
    payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[ISSUE_ALGORITHM])
    # cast 只是把 PyJWT 的宽泛返回类型 dict[str, Any] 收窄成 TokenPayload,方便调用方补全提示。
    # 它不是校验 —— 字段是否真的存在、类型是否真的对,靠的是上面 decode 内的签名/过期校验
    # 和下面 verify_access_token 里的 iss 比对。
    return cast(TokenPayload, payload)


# 验证token
def verify_access_token(token: str) -> TokenPayload:
    payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[ISSUE_ALGORITHM])
    if payload.get('iss') != ISSUER:
        raise BusinessError(code=Code.TOKEN_INVALID, message='无效的token')
    return cast(TokenPayload, payload)


# 从请求投提取token内容
def get_token_from_request(request: Request) -> str:
    token = request.headers.get('token')
    if not token:
        raise BusinessError(code=Code.TOKEN_INVALID, message='未找到token')
    return token

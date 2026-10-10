from typing import Optional, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class UserInfoResponse(BaseModel):
    """获取用户信息的响应体。

    绝不能直接把 User 这个 ORM 对象塞进 success_response:data 的类型是未约束的
    TypeVar(Pydantic 当 Any 处理),序列化时会抛 PydanticSerializationError → 500。
    而且 ORM 对象上有什么列就吐什么列,password 现在是 deferred 才没被带出来,
    一旦别处代码先读了它就会被加载,跟着响应一起泄露给前端。
    写死字段,接口契约才稳。
    """

    username: str
    name: str
    role: str
    email: Optional[str] = Field(None, max_length=50)
    phone: Optional[str] = Field(None, pattern=r'^1[3-9]\d{9}$')
    avatar: Optional[str] = None
    status: int

    # 可以直接从 ORM 模型创建 Pydantic 模型
    model_config = ConfigDict(from_attributes=True)


class UpdateUserRequest(BaseModel):
    """更新自己的资料。字段全部可选,只提交需要改的那几项。

    按产品约定,这里**只放用户自己能改的字段**:name / email / phone / avatar。
    role 和 status 是管理员权限,不在此列;username 是登录凭据,也不许改。
    约束值(max_length 等)与 User 表的列宽保持一致,否则超长会在写库时才炸。

    两条取值约定,路由里必须照做(否则会 500 或误清数据):
      1. 用 model_dump(exclude_unset=True, exclude_none=True) —— 没传的字段、以及
         显式传 null 的字段,都不写回数据库。
      2. 因此**清空一个字段要传空字符串 ''**,不能传 null。
         name 列是 NOT NULL,传 {"name": null} 直接 422 而不是把库里改成 NULL。
    """

    name: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[str] = Field(None, max_length=50)
    # |^$ 是给「清空手机号」留的路:空字符串放行,其余必须符合大陆手机号格式
    phone: Optional[str] = Field(None, pattern=r'^1[3-9]\d{9}$|^$')
    avatar: Optional[str] = Field(None, max_length=50)

    # extra='forbid':拒绝未声明的字段。上面的注释说了哪些字段被刻意排除在外,
    # 传了直接 422,避免「多带一个 role: admin 就把自己提成管理员」这类越权改写。
    model_config = ConfigDict(extra='forbid')

    @model_validator(mode='after')
    def _require_at_least_one_field(self) -> Self:
        # 判定口径必须和路由里的 model_dump 保持一致,否则 {"name": null} 这种
        # 会「校验通过但一个字段都没写」,接口返回成功却什么都没改。
        if not self.model_dump(exclude_unset=True, exclude_none=True):
            raise ValueError('至少要提交一个待更新的字段')
        return self

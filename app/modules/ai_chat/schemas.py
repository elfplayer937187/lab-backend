from typing import List, Literal

from pydantic import BaseModel, ConfigDict, Field


class ChatMessage(BaseModel):
    """
    聊天消息数据模型

    Attributes:
        role: 消息角色（如 user、assistant、system）
        content: 消息内容
    """

    role: Literal["user", "assistant", "system"]
    content: str


class ChatMessageList(BaseModel):
    thread_id: str | None = Field(
        default=None, description="会话 ID,由前端保存;首次不传则自动生成"
    )
    messages: List[ChatMessage]

    model_config = ConfigDict(extra="forbid")

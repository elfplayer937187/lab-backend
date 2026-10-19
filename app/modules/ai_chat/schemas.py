from pydantic import BaseModel, ConfigDict, Field


class ChatMessageList(BaseModel):
    thread_id: str | None = Field(
        default=None, description="会话 ID,由前端保存;首次不传则自动生成"
    )
    content: str = Field(description="消息内容,历史由checkpointer维护")

    model_config = ConfigDict(extra="forbid")

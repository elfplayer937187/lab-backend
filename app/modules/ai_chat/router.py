import json

from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPBearer
from langchain_core.messages import AIMessageChunk
import rich
from sqlalchemy.orm import Session

from app.common.base_response import success_response
from app.common.business_error import BusinessError
from app.database import get_db
from app.modules.ai_chat.schemas import ChatMessageList
from app.modules.ai_chat.services import (
    chat,
    delete_personal_message,
    generate_title,
    get_personal_messages,
    history,
    stream_chat,
)

ai_router = APIRouter(
    prefix="/ai/v1", tags=["大模型相关"], dependencies=[Depends(HTTPBearer())]
)


@ai_router.post("/chat", summary="聊天接口", description="聊天接口")
def chatting(
    payload: ChatMessageList,
    request: Request,
    db: Session = Depends(get_db),
):
    """大模型对话"""
    return success_response(data=chat(payload, request.state.user_id, db))


@ai_router.post("/stream/chat", summary="流式聊天接口", description="流式聊天接口")
def chat_stream(
    payload: ChatMessageList, request: Request, db: Session = Depends(get_db)
):
    """大模型流式对话"""
    thread_id, stream = stream_chat(payload, request.state.user_id, db)

    def sse(data):
        # 把json字符串嵌入文本
        return f"data:{json.dumps(data,ensure_ascii=False)}\n\n"

    def event_generator():
        # 一开始返回一下id
        yield sse(
            {
                "type": "thread_id",
                "thread_id": thread_id,
            }
        )
        try:
            # 这里取出的是(AIMessageChunk, metadata) 二元组
            for chunk, meta in stream:
                rich.print(chunk)
                if isinstance(chunk, AIMessageChunk) and chunk.content:
                    yield sse({"type": "message", "message": chunk.content})

        except Exception as e:
            yield sse({"type": "error", "message": "服务器错误"})
            return
        yield sse({"type": "done"})

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # nginx 下必须,否则会被缓冲
        },
    )


@ai_router.get("/messages/all", summary="获取所有消息", description="获取所有消息")
def get_all_messages(request: Request, db: Session = Depends(get_db)):
    return success_response(
        data=get_personal_messages(user_id=request.state.user_id, db=db)
    )


# 必须放在 /messages/all 之后:否则 FastAPI 会先匹配到 /messages/{thread_id},把 "all" 当成 thread_id
@ai_router.get(
    "/messages/one/{thread_id}", summary="获取历史消息", description="获取历史消息"
)
def get_history_messages(thread_id: str, request: Request):
    return success_response(data=history(thread_id, request.state.user_id))


@ai_router.delete(
    "/delete/message/{thread_id}",
    summary="删除单个会话",
    description="删除标题表记录以及 sqlite 中的会话消息",
)
def delete_message(thread_id: int, request: Request, db: Session = Depends(get_db)):
    return success_response(
        data=delete_personal_message(
            thread_id=thread_id, user_id=request.state.user_id, db=db
        )
    )

from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBearer
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

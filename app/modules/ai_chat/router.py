from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBearer

from app.common.base_response import success_response
from app.modules.ai_chat.schemas import ChatMessageList
from app.modules.ai_chat.services import chat, history

ai_router = APIRouter(
    prefix="/ai/v1", tags=["大模型相关"], dependencies=[Depends(HTTPBearer())]
)


@ai_router.post("/chat", summary="聊天接口", description="聊天接口")
def chatting(payload: ChatMessageList, request: Request):
    content = chat(payload, request.state.user_id)
    return success_response(data=content)


@ai_router.get(
    "/messages/{thread_id}", summary="获取历史消息", description="获取历史消息"
)
def get_history_messages(thread_id: str, request: Request):
    return success_response(data=history(thread_id, request.state.user_id))

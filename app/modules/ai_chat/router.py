from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from app.common.base_response import success_response
from app.modules.ai_chat.schemas import ChatMessageList
from app.modules.ai_chat.services import chat

ai_router = APIRouter(
    prefix="/ai/v1", tags=["大模型相关"], dependencies=[Depends(HTTPBearer())]
)


@ai_router.post("/chat", summary="聊天接口", description="聊天接口")
def chatting(payload: ChatMessageList):
    content = chat(payload)
    return success_response(data=content)

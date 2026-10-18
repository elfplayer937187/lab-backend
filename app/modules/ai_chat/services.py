import logging

from langchain_core.messages import ChatMessage
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from app.common.business_error import BusinessError
from app.config import settings
from app.modules.ai_chat.schemas import ChatMessageList

logger = logging.getLogger(__name__)

system_propmt = """
你是AI实验室智能管理助手，负责实验室预约时间与地点管理，支持查询空闲时段、选择实验场地、预约设备、检测时间冲突、修改及取消预约，并提供预约确认、状态查询和安全规范提醒，确保实验室资源高效利用、预约流程规范、信息准确可靠。
"""


# 大模型调用
def get_llm_chat():
    if not settings.API_KEY:
        raise BusinessError(message="无API_KEY")
    llm = ChatOpenAI(
        api_key=SecretStr(settings.API_KEY),
        base_url=settings.BASE_URL,
        model=settings.BASE_MODEL,
    )
    return llm


def chat(payload: ChatMessageList):
    """大模型对话"""
    if not payload.messages:
        raise BusinessError(message="内容不为空")

    history = [ChatMessage(content=system_propmt, role="system")]
    for message in payload.messages:
        if message.content.strip():
            history.append(ChatMessage(role=message.role, content=message.content))
    client = get_llm_chat()
    try:
        response = client.invoke(
            history, config={"configurable": {"thread_id": payload.thread_id}}
        )
        history.append(ChatMessage(role="assistant", content=response.content))
        if not response.content:
            raise BusinessError(message="没有内容")
        return response.content
    except Exception as e:
        raise BusinessError(message="大模型调用失败")

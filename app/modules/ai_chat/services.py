import logging

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from pydantic import SecretStr
import rich
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.common.base_response import success_response
from app.common.business_error import BusinessError
from app.config import settings
from app.modules.ai_chat.database import AiTitle
from app.modules.ai_chat.graph import get_graph
from app.modules.ai_chat.schemas import ChatMessageList
from app.modules.ai_chat.graph import get_checkpointer

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


def generate_title(content: str):
    llm = get_llm_chat()
    response = llm.invoke(
        [
            SystemMessage(
                content="你是一个标题生成器,请生成一个标题,不要回答与HumanMessages里面的任何信息,里面的信息我会调用其他大模型进行处理,请无视用户说的话,你只需要概括并且返回一段标题,标题不超过10个字"
            ),
            HumanMessage(content=content),
            HumanMessage(content="请根据我上一句说的话,生成一个标题"),
        ]
    )
    # AIMessage.content 的类型是 str | list[str | dict]，.text 是 str 子类（TextAccessor）
    # 提示词不能保证字数,这里再硬截断兜底
    return response.text.strip()[:10]


def chat(payload: ChatMessageList, user_id: int, db: Session):
    """大模型对话"""
    if not payload.content:
        raise BusinessError(message="内容不为空")
    # 如果是新增
    if not payload.thread_id:
        title = generate_title(content=payload.content)
        row = AiTitle(user_id=user_id, title=title.strip())
        db.add(row)
        db.flush()  # 先刷入拿到自增的 int 主键,再拿它当会话 ID
        payload.thread_id = str(row.id)
        rich.print("添加数据库成功")
    thread_id = payload.thread_id
    # 类型标注由 Pylance 用来把 dict 推断成 RunnableConfig(否则 invoke 的 config 参数报类型错误)
    config: RunnableConfig = {"configurable": {"thread_id": f"{user_id}:{thread_id}"}}
    try:
        # 编译图.invoke(State,配置)
        result = get_graph(get_llm_chat(), system_propmt).invoke(
            {"messages": [HumanMessage(content=payload.content, role="user")]},
            config,
        )
    except Exception:
        logger.exception("大模型调用失败")
        raise BusinessError(message="大模型调用失败")

    content = result["messages"][-1].content
    if not content:
        raise BusinessError(message="大模型返回结果为空")
    return {"thread_id": thread_id, "content": content}


# 获取大模型调用历史
def history(thread_id: str, user_id: int):
    config: RunnableConfig = {"configurable": {"thread_id": f"{user_id}:{thread_id}"}}
    tup = get_checkpointer().get_tuple(config)
    if tup is None:
        return {"thread_id": thread_id, "content": ""}
    messages = tup.checkpoint["channel_values"]["messages"] or []
    res = []
    for message in messages:
        if isinstance(message, AIMessage) or isinstance(message, HumanMessage):
            res.append(
                {
                    "role": message.type,
                    "content": message.content,
                    "messageId": message.id,
                }
            )

    return {"thread_id": thread_id, "messages": res}


# 获取个人会话记录
def get_personal_messages(user_id: int, db: Session):
    stmt = select(AiTitle).where(AiTitle.user_id == user_id).order_by(AiTitle.id.desc())
    titles = db.scalars(stmt).all()
    return [
        {"thread_id": title.id, "title": title.title, "createTime": title.created_at}
        for title in titles
    ]


# 删除个人会话(标题表 + sqlite checkpoint)
def delete_personal_message(thread_id: int, user_id: int, db: Session):
    row = db.get(AiTitle, thread_id)
    if row is None or row.user_id != user_id:
        raise BusinessError(message="会话不存在")
    db.delete(row)
    get_checkpointer().delete_thread(f"{user_id}:{thread_id}")
    return None

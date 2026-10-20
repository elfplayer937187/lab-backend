from os import path
import os
import sqlite3

from langchain_core.messages import SystemMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import MessagesState, StateGraph, END, START
from langgraph.pregel.types import RetryPolicy
from langgraph.store.memory import InMemoryStore
from app.config import ROOT_DIR

# 定义全局graph
_graph = None
_checkpointer = None

_checkpointer_path = None
if _checkpointer_path is None:
    if not path.exists(ROOT_DIR / "checkpoint"):
        os.mkdir(ROOT_DIR / "checkpoint")
    _checkpointer_path = ROOT_DIR / "checkpoint" / "checkpoint.db"


def get_checkpointer() -> SqliteSaver:
    global _checkpointer
    if _checkpointer is None:
        # 创建checkpointer
        connection = sqlite3.connect(
            _checkpointer_path or ROOT_DIR / "checkpoint" / "checkpoint.db",
            timeout=30,
            check_same_thread=False,
        )
        _checkpointer = SqliteSaver(connection)
        _checkpointer.setup()
    return _checkpointer


# 创建图
def build_graph(llm: ChatOpenAI, system_prompt: str, checkpointer: SqliteSaver):
    def call_model(state: MessagesState):
        messages = [SystemMessage(content=system_prompt), *state["messages"]]
        response = llm.invoke(messages)
        _ai_message = response.text.strip()
        # 必须返回消息列表:add_messages 会把裸字符串当成 HumanMessage,历史里角色就错了
        return {"messages": AIMessage(content=_ai_message)}

    builder = StateGraph(MessagesState)
    builder.add_node(
        "model",
        call_model,
        retry_policy=RetryPolicy(
            max_attempts=3,
            initial_interval=1.0,
            backoff_factor=2.0,
            max_interval=10.0,
            jitter=True,
        ),
    )
    builder.add_edge(START, "model")
    builder.add_edge("model", END)

    return builder.compile(checkpointer=checkpointer)


def get_graph(llm, system_prompt: str) :
    global _graph
    if _graph is None:
        _graph = build_graph(llm, system_prompt, get_checkpointer())
    return _graph

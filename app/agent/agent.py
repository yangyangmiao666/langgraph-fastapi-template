"""
@Author  : Yang-yang Miao
@Email   : yangyangmiao666@icloud.com
@Time    : 2025/11/18 00:08
@Desc    : LangGraph图配置模块
"""
import logging

from langchain_core.runnables import RunnableConfig
from langfuse import get_client
from langfuse.langchain import CallbackHandler
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.constants import START, END
from langgraph.graph.state import CompiledStateGraph, StateGraph

from app.agent.edge import should_continue
from app.agent.node import llm_node, tool_node
from app.common.constants import LLM_NODE, TOOL_NODE
from app.config import create_postgres_pool_from_config
from app.model.state import MyState

langfuse = get_client()

langfuse_handler = CallbackHandler()


async def my_agent() -> CompiledStateGraph:
    """
    获取单例的LangGraph图实例
    """
    config = RunnableConfig(recursion_limit=25, callbacks=[langfuse_handler])
    # 使用 AsyncPostgresSaver
    checkpointer = AsyncPostgresSaver(create_postgres_pool_from_config())
    # 初始化检查点保存器（这会创建必要的表结构）
    await checkpointer.setup()

    # 构建图
    graph = (
        StateGraph(MyState)
        .add_node(LLM_NODE, llm_node)
        .add_node(TOOL_NODE, tool_node)
        .add_edge(START, LLM_NODE)
        .add_conditional_edges(LLM_NODE, should_continue, [TOOL_NODE, END])
        .add_edge(TOOL_NODE, LLM_NODE)
        .compile(checkpointer=checkpointer)
        .with_config(config=config)
    )
    logging.info(f"graph 图实例:{graph.get_graph(xray=True).draw_mermaid()}")
    return graph

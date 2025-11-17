"""
@Author  : Yang-yang Miao
@Email   : yangyangmiao666@icloud.com
@Time    : 2025/11/18 00:13
@Desc    : node.py
"""
import logging

from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import ToolNode

from app.config import create_model_from_config
from app.model.state import MyState
from app.tools import user_tools
from app.tools.mcp_client import my_mcp_client


async def llm_node(state: MyState) -> dict:
    """
    llm节点
    :param state: 状态
    :type state: MyState
    :return: 更新状态
    :rtype: dict
    """
    logging.info(f"llm_node节点 state: {state}")
    mcp_tools = await my_mcp_client.get_mcp_tools()
    llm = create_model_from_config().bind_tools(user_tools + mcp_tools)
    config = RunnableConfig(configurable={"thread_id": state.thread_id})
    messages = state.messages
    response = await llm.ainvoke(messages, config)
    logging.info(f"llm_node节点 response: {response}")
    return {"messages": response, "thread_id": state.thread_id}


async def tool_node(state: MyState) -> ToolNode:
    """
    tool节点
    :param state: 状态
    :type state: MyState
    :return: 状态
    :rtype: dict
    """
    logging.info(f"tool_node节点，state：{state}")
    mcp_tools = await my_mcp_client.get_mcp_tools()
    # 创建工具节点
    tool_node_instance = ToolNode(user_tools + mcp_tools)
    return tool_node_instance

"""
@Author  : Yang-yang Miao
@Email   : yangyangmiao666@icloud.com
@Time    : 2025/11/18 00:13
@Desc    : edge.py
"""
import logging

from langgraph.constants import END

from app.common.constants import TOOL_NODE
from app.model import MyState


def should_continue(state: MyState) -> str:
    """
    llm节点和tool节点之间的边
    :param state: 状态
    :type state: MyState
    :return: 下一个节点
    :rtype: str
    """
    """Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""

    messages = state.messages
    last_message = messages[-1]

    if last_message.tool_calls:
        logging.info(f"检测到工具调用: {last_message.tool_calls}")
        return TOOL_NODE
    logging.info("LLM没有工具调用，回复用户")
    return END

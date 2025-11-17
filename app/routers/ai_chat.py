"""
@Author  : Yang-yang Miao
@Email   : yangyangmiao666@icloud.com
@Time    : 2025/11/18 00:13
@Desc    : ai_chat.py
"""
import logging
from functools import lru_cache

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from langfuse import observe, propagate_attributes
from langgraph.graph.state import CompiledStateGraph

from app.agent.agent import my_agent
from app.service import AiChatService
from app.service.impl import OpenAiChatServiceImpl

router = APIRouter()

tags = ["ai_chat"]


# 依赖注入
@lru_cache(maxsize=1)
def get_chat_service(graph: CompiledStateGraph = Depends(my_agent)):
    return OpenAiChatServiceImpl(graph=graph)


@observe()
@router.get(path="/ai/chat", tags=tags)
async def ai_chat_controller(message: str = "介绍一下自己",
                             user_id: str = "Yang-yang Miao",
                             session_id: str = "1",
                             ai_chat_service: AiChatService = Depends(get_chat_service)) -> str:
    """
    AI聊天接口控制器

    接收用户消息并返回AI回复

    Args:
        :param message: 用户输入的消息，默认为"介绍一下自己"
        :param ai_chat_service: 依赖注入
        :param user_id: 用户ID，默认为"Yang-yang Miao"
        :param session_id: 会话ID，默认为"1"

    Returns:
        AI的回复内容
    """
    with propagate_attributes(user_id=user_id):
        logging.info(f"收到聊天请求: {message}")
        try:
            response = await ai_chat_service.chat(message, session_id)
            logging.info(f"聊天响应成功，response: {response}")
            return response
        except Exception as e:
            logging.error(f"聊天处理失败: {str(e)}")
            raise


@router.get(path="/ai/chat-stream", tags=tags)
async def ai_chat_stream_controller(message: str = "介绍一下自己",
                                    user_id: str = "Yang-yang Miao",
                                    session_id: str = "1",
                                    ai_chat_service: AiChatService = Depends(get_chat_service)) -> StreamingResponse:
    """
    AI聊天流式接口控制器

    接收用户消息并返回AI回复
    Args:
        :param message: 用户输入的消息，默认为"介绍一下自己"
        :param user_id: 用户ID，默认为"Yang-yang Miao"
        :param session_id: 会话ID，默认为"1"
        :param ai_chat_service: 依赖注入

    Returns:
        AI的回复内容
    """
    with propagate_attributes(user_id=user_id):
        logging.info(f"收到流式聊天请求: {message}")
        try:
            # 获取流式响应并确保编码正确
            response = await ai_chat_service.chat_stream(message, session_id)
            logging.info(f"流式聊天响应成功，response: {response}")
            return response
        except Exception as e:
            logging.error(f"流式聊天处理失败: {str(e)}")
            raise


@router.get(path="/ai/get-current-state", tags=tags)
async def get_current_state(session_id: str = "1",
                            ai_chat_service: AiChatService = Depends(get_chat_service)) -> str:
    """
    获取AI聊天服务的当前状态

    Args:
        :param session_id: 会话ID，默认为"1"
        :param ai_chat_service: AI聊天服务实例，通过依赖注入获取

    Returns:
        str: 返回AI聊天服务的当前状态信息
    """
    return await ai_chat_service.get_current_state(session_id)


@router.get(path="/ai/get-history-state", tags=tags)
async def get_history_state(session_id: str = "1",
                            ai_chat_service: AiChatService = Depends(get_chat_service)) -> str:
    """
    获取AI聊天历史状态的异步接口函数

    该函数通过FastAPI路由装饰器定义了一个GET请求接口，用于获取当前AI聊天服务的历史状态信息。

    Args:
        :param session_id: 会话ID，默认为"1"
        :param ai_chat_service: AI聊天服务实例，通过依赖注入方式获取

    Returns:
        str: 返回AI聊天服务的历史状态信息字符串
    """
    return await ai_chat_service.get_history_state(session_id)

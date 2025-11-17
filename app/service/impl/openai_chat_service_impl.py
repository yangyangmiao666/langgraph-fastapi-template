"""
@Author  : Yang-yang Miao
@Email   : yangyangmiao666@icloud.com
@Time    : 2025/11/18 00:15
@Desc    : openai_chat_service_impl.py
"""
import logging
from typing import AsyncIterator

from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage, BaseMessage, SystemMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph.state import CompiledStateGraph
from langgraph.types import StateSnapshot

from app.config.response_config import ResponseConfig
from app.model.state import MyState
from app.service.ai_chat_service import AiChatService


class OpenAiChatServiceImpl(AiChatService):
    """
    AI聊天服务实现类，负责初始化AI代理并处理用户聊天请求。
    """
    _graph: CompiledStateGraph

    def __init__(self, graph: CompiledStateGraph):
        # 获取单例图实例
        self._graph = graph

    async def chat(self, user_input: str, session_id: str) -> str:
        """
        处理用户聊天输入并返回AI的响应。

        :param user_input: 用户输入
        :param session_id: 会话ID
        :return: AI的响应结果
        """
        # 配置
        config = RunnableConfig(configurable={"thread_id": session_id})

        chat_state = MyState(messages=[HumanMessage(content=user_input)], thread_id=session_id)
        response = await self._graph.ainvoke(chat_state, config)
        logging.info(f"response 结果:{response}")
        ai_message = response.get("messages")[-1]
        return str(ai_message.content)

    async def chat_stream(self, user_input: str, session_id: str) -> StreamingResponse:
        """
        处理用户聊天输入并返回AI的响应。

        :param user_input: 用户输入
        :return: AI的响应结果
        """
        chat_messages: list[BaseMessage] = [
            SystemMessage(content="你是一个全能的人工智能助手，你的名字叫糯米,你可以调用工具来解决用户的问题"),
            HumanMessage(content=user_input)
        ]
        chat_state = MyState(messages=chat_messages, thread_id=session_id)
        logging.info("开始流式输出...")
        # 使用ResponseConfig创建流式响应，确保浏览器兼容性
        return ResponseConfig.create_streaming_response(
            content=self.response_streamer(chat_state=chat_state),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "text/event-stream; charset=utf-8"
            }
        )

    async def response_streamer(self, chat_state: MyState) -> AsyncIterator[str]:
        config = RunnableConfig(configurable={"thread_id": chat_state.thread_id})
        async for chunk in self._graph.astream(input=chat_state, config=config, stream_mode="messages"):
            # chunk 是一个元组 (message_chunk, metadata)
            message_chunk, metadata = chunk
            # logging.info(f"消息类型: {type(message_chunk)}")
            # logging.info(f"元数据: {metadata}")
            if not isinstance(message_chunk, AIMessage):
                continue
            if hasattr(message_chunk, 'content'):
                content = message_chunk.content
                # 使用统一的编码配置
                if isinstance(content, str):
                    # logging.info(f"输出内容: {content}")
                    yield ResponseConfig.encode_content(content)
                else:
                    content_str = str(content)
                    # logging.info(f"输出内容(转换): {content_str}")
                    yield ResponseConfig.encode_content(content_str)
            else:
                content_str = str(message_chunk)
                # logging.info(f"输出消息: {content_str}")
                yield ResponseConfig.encode_content(content_str)

    async def get_current_state(self, session_id: str) -> str:
        config: RunnableConfig = RunnableConfig(configurable={"thread_id": session_id})
        state_snapshot: StateSnapshot = await self._graph.aget_state(config=config)
        logging.info(f"state_snapshot 状态快照:{state_snapshot}")
        return str(state_snapshot)

    async def get_history_state(self, session_id: str) -> str:
        config: RunnableConfig = RunnableConfig(configurable={"thread_id": session_id})
        async_iterator: AsyncIterator[StateSnapshot] = self._graph.aget_state_history(config=config)
        state_snapshots: list[StateSnapshot] = []
        async for state_snapshot in async_iterator:
            state_snapshots.append(state_snapshot)
        logging.info(f"state_snapshots 状态快照历史记录:{state_snapshots}")
        return str(state_snapshots)

"""
@Author  : Yang-yang Miao
@Email   : yangyangmiao666@icloud.com
@Time    : 2025/11/18 00:14
@Desc    : ai_chat_service.py
"""
from abc import abstractmethod, ABC

from fastapi.responses import StreamingResponse


class AiChatService(ABC):
    @abstractmethod
    async def chat(self, user_input: str, session_id: str) -> str:
        pass

    @abstractmethod
    async def chat_stream(self, user_input: str, session_id: str) -> StreamingResponse:
        pass

    @abstractmethod
    async def get_current_state(self, session_id: str) -> str:
        pass

    @abstractmethod
    async def get_history_state(self, session_id: str) -> str:
        pass
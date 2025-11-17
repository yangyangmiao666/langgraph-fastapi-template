"""
@Author  : Yang-yang Miao
@Email   : yangyangmiao666@icloud.com
@Time    : 2025/11/18 00:13
@Desc    : state.py
"""
from typing import Annotated, Optional

from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
from pydantic import BaseModel


class MyState(BaseModel):
    messages: Annotated[list[BaseMessage], add_messages]
    thread_id: Optional[str] = None

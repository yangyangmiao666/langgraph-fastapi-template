"""
@Author  : Yang-yang Miao
@Email   : yangyangmiao666@icloud.com
@Time    : 2025/11/18 00:16
@Desc    : my_mcp_client.py
"""
import os

from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.sessions import SSEConnection

from app.common.constants import MCP_BASE_URL, MCP_ENDPOINT


async def get_mcp_tools() -> list[BaseTool]:
    """
    获取MCP工具
    :param nio_user_info: NIO用户信息
    :return: MCP工具
    """
    multi_server_mcp_client = MultiServerMCPClient(
        {
            "mcp_server": SSEConnection(
                url=os.getenv(MCP_BASE_URL) + os.getenv(MCP_ENDPOINT),
                transport="sse",
                timeout=60,
                headers={
                    "Authorization": "Bearer xxx",
                    "Content-Type": "application/json"
                },
            )
        }
    )
    mcp_tools = await multi_server_mcp_client.get_tools()
    return mcp_tools

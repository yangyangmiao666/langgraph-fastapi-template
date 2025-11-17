"""
@Author  : Yang-yang Miao
@Email   : yangyangmiao666@icloud.com
@Time    : 2025/11/18 00:16
@Desc    : user_tools.py
"""
import logging

from langchain_core.tools import tool

TOOL_GET_ALL_USERS = "get_all_users"


@tool(name_or_callable=TOOL_GET_ALL_USERS, description="获取全部用户")
def get_all_users() -> dict[str, list[dict[str, str | int]]]:
    logging.info("工具调用 => get_all_users")
    """获取全部用户"""
    return {
        "users": [
            {"name": "Alice", "age": 25},
            {"name": "Bob", "age": 30},
            {"name": "Charlie", "age": 35},
        ]
    }


user_tools = [get_all_users]

# 导出工具映射，方便其他模块使用
user_tool_map = {
    TOOL_GET_ALL_USERS: get_all_users
}

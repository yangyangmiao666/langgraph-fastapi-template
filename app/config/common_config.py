"""
@Author  : Yang-yang Miao
@Email   : yangyangmiao666@icloud.com
@Time    : 2025/11/18 00:13
@Desc    : common_config.py
"""
import os
from functools import lru_cache

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langfuse import Langfuse
from psycopg_pool import AsyncConnectionPool
from pydantic import SecretStr

from app.common.constants import *

# 加载.env文件
load_dotenv()


@lru_cache(maxsize=1)
def create_model_from_config() -> ChatOpenAI:
    """
    从.env文件创建OpenAI实例

    Returns:
        ChatOpenAI: 配置好的OpenAI实例
    """
    # 直接从环境变量读取配置
    api_key = os.getenv(OPENAI_API_KEY)
    base_url = os.getenv(OPENAI_BASE_URL)
    model_name = os.getenv(OPENAI_MODEL_NAME, 'deepseek-v3')

    # 创建ChatOpenAI实例
    model = ChatOpenAI(
        api_key=SecretStr(api_key),
        base_url=base_url,
        model=model_name,
    )
    return model


@lru_cache(maxsize=1)
def create_postgres_pool_from_config():
    db_uri = f"postgresql://{os.getenv(POSTGRES_USER)}:{os.getenv(POSTGRES_PASSWORD)}@{os.getenv(POSTGRES_HOST)}:{os.getenv(POSTGRES_PORT)}/{os.getenv(POSTGRES_DB)}?sslmode=disable"
    connection_kwargs = {"autocommit": True, "prepare_threshold": 0}

    pool = AsyncConnectionPool(conninfo=db_uri, max_size=20, kwargs=connection_kwargs)
    return pool


@lru_cache(maxsize=1)
def create_langfuse_from_config():
    """
    从.env文件创建Langfuse实例
    """
    langfuse = Langfuse(
        secret_key=os.getenv(LANGFUSE_SECRET_KEY),
        public_key=os.getenv(LANGFUSE_PUBLIC_KEY),
        host=os.getenv(LANGFUSE_HOST, 'https://cloud.langfuse.com')
    )
    return langfuse

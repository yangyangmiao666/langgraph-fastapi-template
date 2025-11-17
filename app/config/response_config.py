"""
@Author  : Yang-yang Miao
@Email   : yangyangmiao666@icloud.com
@Time    : 2025/11/18 00:13
@Desc    : response_config.py
"""
from typing import Dict, AsyncIterator

from fastapi.responses import StreamingResponse


class ResponseConfig:
    """响应配置类"""

    # 默认编码配置
    DEFAULT_CHARSET = "utf-8"
    DEFAULT_MEDIA_TYPE = f"text/plain; charset={DEFAULT_CHARSET}"
    DEFAULT_HEADERS = {"Content-Type": DEFAULT_MEDIA_TYPE}

    # JSON响应配置
    JSON_MEDIA_TYPE = f"application/json; charset={DEFAULT_CHARSET}"
    JSON_HEADERS = {"Content-Type": JSON_MEDIA_TYPE}

    @classmethod
    def create_streaming_response(
            cls,
            content: AsyncIterator[str],
            media_type: str = None,
            headers: Dict[str, str] = None
    ) -> StreamingResponse:
        """
        创建统一配置的流式响应

        Args:
            content: 流式内容生成器
            media_type: 媒体类型，默认使用text/plain; charset=utf-8
            headers: 额外的响应头，会与默认头合并

        Returns:
            配置好的StreamingResponse
        """
        # 使用默认配置
        final_media_type = media_type or cls.DEFAULT_MEDIA_TYPE
        final_headers = cls.DEFAULT_HEADERS.copy()

        # 合并额外的头部
        if headers:
            final_headers.update(headers)

        return StreamingResponse(
            content=content,
            media_type=final_media_type,
            headers=final_headers
        )

    @classmethod
    def encode_content(cls, content: str) -> str:
        """
        统一编码内容

        Args:
            content: 要编码的内容

        Returns:
            编码后的内容
        """
        return str(content).encode(cls.DEFAULT_CHARSET).decode(cls.DEFAULT_CHARSET)

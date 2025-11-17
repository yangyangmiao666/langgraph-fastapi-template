"""
@Author  : Yang-yang Miao
@Email   : yangyangmiao666@icloud.com
@Time    : 2025/11/18 00:17
@Desc    : main.py
"""
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import ai_chat

# 创建 FastAPI 应用实例
app = FastAPI(
    title="LangGraph Demo API",
    description="A comprehensive demonstration project showcasing LangGraph and LangChain capabilities",
    version="0.1.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(ai_chat.router, prefix="/api")

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)d - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
    encoding="utf-8"
)


@app.get("/")
async def root():
    """根路径健康检查"""
    return {"message": "LangGraph Demo API is running!", "status": "healthy"}


@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "healthy", "service": "langgraph-demo"}


if __name__ == "__main__":
    import uvicorn

    logging.info("启动 FastAPI 应用...")
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8001,
        reload=True,
        log_level="info"
    )

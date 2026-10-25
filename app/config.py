import os
from pathlib import Path

from pydantic_settings import BaseSettings

ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = ROOT_DIR / ".env"


class Settings(BaseSettings):
    # 必需项,无默认值 —— 从 .env 读取。缺失时启动即报错,不要在这里写死连接串
    DATABASE_URL: str

    # JWT 配置
    JWT_SECRET_KEY: str
    JWT_EXPIRATION_HOURS: int = 24
    JWT_ALGORITHM: str = "HS256"
    # 是否打印 SQLAlchemy 生成的 SQL,开发时开启便于调试
    DB_ECHO: bool = True
    # ai
    BASE_URL: str = "https://api.agnes-ai.cn/v1"
    API_KEY: str
    BASE_MODEL: str = "agnes-2.5-flash"
    # LangSmith 监测(可选,留空则不开启)
    LANGSMITH_API_KEY: str = ""
    LANGSMITH_TRACING: str = "false"
    LANGSMITH_PROJECT: str = "ai-chat"
    model_config = {
        "env_file": ENV_FILE,
        "env_file_encoding": "utf-8",
        # .env 中多余的键不报错,便于逐步补充配置项
        "extra": "ignore",
    }


# DATABASE_URL 等无默认值的字段由 pydantic-settings 在运行时从 .env 注入,
# 静态分析器看不到这一步,会误报「缺少参数」,故忽略 call-arg。
settings = Settings()  # type: ignore[call-arg]

# LangChain 只从进程环境变量读取 LangSmith 配置(不经过 pydantic-settings),
# 故在这里集中回写一次,业务代码零改动。
if settings.LANGSMITH_API_KEY:
    os.environ["LANGSMITH_API_KEY"] = settings.LANGSMITH_API_KEY
    os.environ["LANGSMITH_TRACING"] = settings.LANGSMITH_TRACING
    os.environ["LANGSMITH_PROJECT"] = settings.LANGSMITH_PROJECT


# 文件上传路径
UPLOAD_DIR = ROOT_DIR / "uploads"

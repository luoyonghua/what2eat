# /src/core/config.py
from functools import lru_cache
from typing import Literal

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "What to Eat"
    app_version: str = "1.0.0"
    app_debug: bool = False

    # 数据库类型
    db_type: Literal["sqlite", "postgresql", "mysql"] = "sqlite"

    #PostgreSQL 配置
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "postgres"
    db_password: str = "postgres"
    db_name: str = "what2eat"

    #MySQL 配置
    mysql_host: str = "localhost"
    mysql_port: int = 3306
    mysql_user: str = "root"
    mysql_password: str = "123456"
    mysql_db: str = "what2eat"

    #连接池配置（仅postgres）
    pool_size: int = 20             # 连接池大小    
    max_overflow: int = 10          # 最大溢出连接数
    pool_timeout: int = 30          # 连接池超时时间
    pool_pre_ping: bool = True      # 是否启用连接池预ping

    #可选调优参数
    pool_recycle: int = 3600       # 连接池回收时间
    pool_use_lifo: bool = False     # 连接池取连接顺序（FIFO or LIFO）可提高高并发性能
    echo: bool = False          # 是否输出SQL语句日志

    #SQLite 配置
    sqlite_path: str = "./data/what2eat.sqlite3"

    @computed_field
    @property
    def database_url(self) -> str:
        if self.db_type == "postgresql":
            return (
                f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
            )
        elif self.db_type == "mysql":
            return f"mysql+aiomysql://{self.mysql_user}:{self.mysql_password}@{self.mysql_host}:{self.mysql_port}/{self.mysql_db}"
        elif self.db_type == "sqlite":  # sqlite
            return f"sqlite+aiosqlite:///{self.sqlite_path}"
        else:
            raise ValueError("Unsupported database type: {self.db_type}")

    @computed_field
    @property
    def engine_options(self) -> dict:
        """
            统一封装 engine options，供 create_async_engine 使用
        """
        if self.db_type == "postgresql":
            return {
                "pool_size": self.pool_size,
                "max_overflow": self.max_overflow,
                "pool_timeout": self.pool_timeout,
                "pool_pre_ping": self.pool_pre_ping,
                "pool_recycle": self.pool_recycle,
                "pool_use_lifo": self.pool_use_lifo,
                "echo": self.echo
            }
        # SQLite 和 MySQL 不需要连接池配置，返回最小参数
        return {"echo": self.echo}

    # JWT 配置
    jwt_secret: str = "your_secret_key"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8",case_sensitive=False)


# @lru_cache()
# def get_settings() -> Settings:
#     return Settings()

# settings = get_settings()
settings = Settings()
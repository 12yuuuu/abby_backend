from functools import lru_cache
from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    """Global Configuration"""

    openapi_url: str | None = None  # OpenAPI URL (None means disabled, enabled only in dev)
    docs_url: str | None = None  # Swagger UI URL (None means disabled, enabled only in dev)
    redoc_url: str | None = None  # ReDoc UI URL (None means disabled, enabled only in dev)

    datasource_url: str  # Database connection URL
    db_pool_size: int = 5  # Database connection pool size
    db_pool_max_overflow: int = 5  # Maximum overflow for the database connection pool
    is_print_sql: bool = False  # Whether to print SQL logs

    langsmith_tracing: str = "true"
    langsmith_endpoint: str = "https://api.smith.langchain.com"
    langsmith_api_key: str | None = None
    langsmith_project: str | None = None
    openai_api_key: str | None = None

    deepseek_url: str | None = None
    deepseek_api_key: str | None = None
    deepseek_model: str | None = None

    class Config:
        env_file = ".env"
        env_ignore_empty = True


@lru_cache
def get_setting() -> Setting:
    """Get global configuration"""
    return Setting()

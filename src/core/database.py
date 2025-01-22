import time
from loguru import logger
from sqlalchemy import Engine
from sqlmodel import SQLModel, create_engine, Field, BigInteger, Boolean

from src.core.setting import get_setting

setting = get_setting()

# PostgreSQL
engine = create_engine(
    setting.datasource_url,
    pool_size=setting.db_pool_size,
    max_overflow=setting.db_pool_max_overflow,
    echo=setting.is_print_sql,
)

def init_db():
    # Database models
    # import src.model

    logger.info("[Database] Initializing...")
    SQLModel.metadata.create_all(engine)
    logger.info("[Database] Initialization complete")


def get_engine() -> Engine:
    return engine

class BaseTable(SQLModel):
    """Base table class"""

    id: int | None = Field(sa_type=BigInteger, default=None, primary_key=True)
    create_timestamp: int = Field(
        sa_type=BigInteger,
        default_factory=lambda: time.time_ns() // 1000000,
        sa_column_kwargs={"comment": "Creation timestamp"},
    )
    update_timestamp: int = Field(
        sa_type=BigInteger,
        default_factory=lambda: time.time_ns() // 1000000,
        sa_column_kwargs={"comment": "Update timestamp"},
    )
    is_deleted: bool = Field(
        sa_type=Boolean, default=False, sa_column_kwargs={"comment": "Is deleted"}
    )

    def mark_update(self) -> None:
        self.update_timestamp = time.time_ns() // 1000000

    def mark_delete(self) -> None:
        self.is_deleted = True
        self.update_timestamp = time.time_ns() // 1000000

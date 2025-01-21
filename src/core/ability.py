from loguru import logger
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from src.core.database import init_db
from src.core.setting import get_setting


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI Lifecycle"""
    logger.add("logs/info.log", rotation="00:00", retention="7 days")
    logger.add("logs/error.log", rotation="00:00", retention="7 days", level="ERROR")
    # # Add configuration information log
    logger.info("Current configuration: {}", get_setting())

    init_db()
    logger.info("[Service] Started")
    yield
    logger.info("[Service] Stopped")

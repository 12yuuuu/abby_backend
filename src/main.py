import time
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from sqlalchemy.exc import SQLAlchemyError

from src.core.ability import lifespan
from src.core.schema import ErrorResp
from src.core.setting import get_setting
from src.core.exception import (
    BizException,
    SysException,
    biz_exception_handler,
    http_exception_handler,
    request_validation_handler,
    response_validation_handler,
    exception_handler,
    sql_exception_handler,
    sys_exception_handler,
)
from src.router.client_router import router as client_router
from src.router.conversation_router import router as conversation_router
from src.router.message_router import router as message_router
from src.router.sku_router import router as sku_router
from src.router.spu_router import router as spu_router
from src.router.transaction_router import router as transaction_router
from src.router.agent_router import router as agent_router

settings = get_setting()

# Initialize FastAPI app
app = FastAPI(
    lifespan=lifespan,
    title="Project Title",
    summary="Project Summary",
    openapi_url=settings.openapi_url,
    docs_url=settings.docs_url,
    redoc_url=settings.redoc_url,
    responses={"400": {"model": ErrorResp}, "500": {"model": ErrorResp}},
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handling
app.add_exception_handler(BizException, biz_exception_handler)
app.add_exception_handler(SysException, sys_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, exception_handler)
app.add_exception_handler(RequestValidationError, request_validation_handler)
app.add_exception_handler(ResponseValidationError, response_validation_handler)
app.add_exception_handler(SQLAlchemyError, sql_exception_handler)

# Route Rules
app.include_router(client_router)
app.include_router(conversation_router)
app.include_router(message_router)
app.include_router(sku_router)
app.include_router(spu_router)
app.include_router(transaction_router)
app.include_router(agent_router)

@app.get("/basic-path/", summary="Check", response_model=dict[str, object])
async def root():
    logger.info("Global Settings: {}", settings)
    return {
        "message": "Service is running...",
        "timestamp": time.time_ns() // 1000000,
    }

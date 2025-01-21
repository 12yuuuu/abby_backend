from loguru import logger
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from src.core.schema import ErrorResp


class BizException(Exception):
    """Business exception base class"""

    def __init__(self, message: str):
        self.message = message


class SysException(Exception):
    """System exception base class"""

    def __init__(self, message: str):
        self.message = message


async def biz_exception_handler(request: Request, exc: BizException):
    """Business exception handler"""
    resp = ErrorResp(summary="Business error", message=f"{exc.message}")
    return JSONResponse(status_code=400, content=resp.model_dump())


async def sys_exception_handler(request: Request, exc: SysException):
    """System exception handler"""
    resp = ErrorResp(summary="System error", message=f"{exc.message}")
    return JSONResponse(status_code=500, content=resp.model_dump())


async def http_exception_handler(request: Request, exc: HTTPException):
    """HTTP exception handler"""
    resp = ErrorResp(summary="Custom error", message=f"{exc.detail}")
    return JSONResponse(status_code=exc.status_code, content=resp.model_dump())


async def request_validation_handler(request: Request, err: RequestValidationError):
    """Parameter validation exception handler"""
    error_messages = []
    for error in err.errors():
        error_messages.append(f"{error['loc'][1]}: {error['msg']}")

    resp = ErrorResp(summary="Parameter error", message="\n".join(error_messages))
    return JSONResponse(status_code=400, content=resp.model_dump())


async def response_validation_handler(request: Request, err: ResponseValidationError):
    """Response binding exception"""
    resp = ErrorResp(summary="Response result error", message=f"{err}")
    logger.error("Response result error, [{}] {} {}", request.method, request.url, err)
    return JSONResponse(status_code=500, content=resp.model_dump())


async def sql_exception_handler(request: Request, err: SQLAlchemyError):
    """Database exception handler"""
    if isinstance(err, NoResultFound):
        resp = ErrorResp(summary="Data error", message=f"Data not found: {err}")
    else:
        resp = ErrorResp(summary="Database error", message=f"{err}")
        logger.error("Database error, [{}] {} {}", request.method, request.url, err)
    return JSONResponse(status_code=500, content=resp.model_dump())


async def exception_handler(request: Request, err: Exception):
    """Global exception handler"""
    body = ""
    if (
        request.method in ("POST", "PUT", "PATCH")
        and request.headers.get("Content-Type") == "application/json"
    ):
        try:
            body = await request.body()
        except Exception:
            pass
    logger.error("Unknown exception, [{}] {} {}", request.method, request.url, body, err)
    resp = ErrorResp(summary="Unknown exception", message=f"{err}")
    return JSONResponse(status_code=500, content=resp.model_dump())

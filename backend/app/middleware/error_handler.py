"""
全局异常处理中间件
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from redis.exceptions import RedisError
from app.core.exceptions import APIException, BusinessException
from app.core.codes import ResponseCode, ResponseMessage, get_http_status
from app.core.logger import logger
import traceback


async def business_exception_handler(request: Request, exc: BusinessException) -> JSONResponse:
    """业务异常处理"""
    logger.warning(f"Business Exception: {exc.message} | Path: {request.url.path}")
    
    return JSONResponse(
        status_code=get_http_status(exc.code),
        content={
            "code": exc.code,
            "message": exc.message,
            "data": exc.data
        }
    )


async def api_exception_handler(request: Request, exc: APIException) -> JSONResponse:
    """API异常处理"""
    logger.warning(f"API Exception: {exc.message} | Path: {request.url.path}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.code,
            "message": exc.message,
            "data": exc.data
        }
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """HTTP异常处理"""
    logger.warning(f"HTTP Exception: {exc.detail} | Status: {exc.status_code} | Path: {request.url.path}")
    
    # 映射HTTP状态码到业务状态码
    code_mapping = {
        400: ResponseCode.BAD_REQUEST,
        401: ResponseCode.UNAUTHORIZED,
        403: ResponseCode.FORBIDDEN,
        404: ResponseCode.RESOURCE_NOT_FOUND,
        500: ResponseCode.INTERNAL_ERROR,
    }
    
    business_code = code_mapping.get(exc.status_code, ResponseCode.INTERNAL_ERROR)
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": business_code,
            "message": exc.detail or ResponseMessage.get_message(business_code),
            "data": None
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """参数验证异常处理"""
    logger.warning(f"Validation Error: {exc} | Path: {request.url.path}")
    
    errors = exc.errors()
    # 格式化验证错误信息
    error_messages = []
    simplified_errors = []
    
    for error in errors:
        loc = error.get("loc", [])
        # 跳过 'body' 前缀，获取字段名
        field_parts = [str(l) for l in loc if l not in ('body',)]
        field = " -> ".join(field_parts) if field_parts else "request"
        
        # 获取错误消息，处理可能的异常对象
        msg = error.get("msg", "Unknown error")
        if isinstance(msg, Exception):
            msg = str(msg)
        else:
            msg = str(msg)
        
        error_messages.append(f"{field}: {msg}")
        simplified_errors.append({
            "field": field,
            "message": msg,
            "type": error.get("type", "unknown")
        })
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "code": ResponseCode.VALIDATION_ERROR,
            "message": "; ".join(error_messages),
            "data": simplified_errors
        }
    )


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    """数据库异常处理"""
    logger.error(f"Database Error: {str(exc)} | Path: {request.url.path}")
    logger.error(traceback.format_exc())
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": ResponseCode.DATABASE_ERROR,
            "message": ResponseMessage.get_message(ResponseCode.DATABASE_ERROR),
            "data": None
        }
    )


async def redis_exception_handler(request: Request, exc: RedisError) -> JSONResponse:
    """Redis异常处理"""
    logger.error(f"Redis Error: {str(exc)} | Path: {request.url.path}")
    logger.error(traceback.format_exc())
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": ResponseCode.REDIS_ERROR,
            "message": ResponseMessage.get_message(ResponseCode.REDIS_ERROR),
            "data": None
        }
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """通用异常处理"""
    logger.error(f"Unhandled Exception: {str(exc)} | Path: {request.url.path}")
    logger.error(traceback.format_exc())
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": ResponseCode.INTERNAL_ERROR,
            "message": ResponseMessage.get_message(ResponseCode.INTERNAL_ERROR),
            "data": None
        }
    )


def register_exception_handlers(app):
    """注册所有异常处理器"""
    app.add_exception_handler(BusinessException, business_exception_handler)
    app.add_exception_handler(APIException, api_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
    app.add_exception_handler(RedisError, redis_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)


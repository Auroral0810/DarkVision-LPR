"""
统一响应格式和工具函数
"""
from typing import Any, Optional, Union, Dict
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from app.core.codes import ResponseCode, ResponseMessage, get_http_status


class UnifiedResponse(BaseModel):
    """统一响应模型"""
    code: int  # 业务状态码
    message: str  # 响应消息
    data: Optional[Any] = None  # 响应数据
    
    class Config:
        json_schema_extra = {
            "example": {
                "code": 20000,
                "message": "操作成功",
                "data": {"id": 1, "name": "示例"}
            }
        }


def success(
    data: Any = None,
    message: str = None,
    code: ResponseCode = ResponseCode.SUCCESS
) -> JSONResponse:
    """
    成功响应
    
    Args:
        data: 响应数据
        message: 自定义消息（可选）
        code: 业务状态码
        
    Returns:
        JSONResponse
    """
    return JSONResponse(
        status_code=get_http_status(code),
        content={
            "code": code,
            "message": message or ResponseMessage.get_message(code),
            "data": data
        }
    )


def error(
    code: ResponseCode = ResponseCode.INTERNAL_ERROR,
    message: str = None,
    data: Any = None
) -> JSONResponse:
    """
    错误响应
    
    Args:
        code: 业务状态码
        message: 自定义错误消息（可选）
        data: 额外的错误信息
        
    Returns:
        JSONResponse
    """
    return JSONResponse(
        status_code=get_http_status(code),
        content={
            "code": code,
            "message": message or ResponseMessage.get_message(code),
            "data": data
        }
    )


def success_response(
    data: Any = None,
    message: str = "操作成功",
    code: int = ResponseCode.SUCCESS
) -> Dict:
    """
    成功响应（返回字典，用于路由函数）
    
    Args:
        data: 响应数据
        message: 响应消息
        code: 业务状态码
        
    Returns:
        Dict
    """
    return {
        "code": code,
        "message": message,
        "data": data
    }


def error_response(
    code: ResponseCode = ResponseCode.INTERNAL_ERROR,
    message: str = None,
    data: Any = None
) -> Dict:
    """
    错误响应（返回字典）
    
    Args:
        code: 业务状态码
        message: 错误消息
        data: 额外信息
        
    Returns:
        Dict
    """
    return {
        "code": code,
        "message": message or ResponseMessage.get_message(code),
        "data": data
    }


# 快捷方法
def success_created(data: Any = None, message: str = "创建成功"):
    """创建成功"""
    return success(data, message, ResponseCode.CREATED)


def success_updated(data: Any = None, message: str = "更新成功"):
    """更新成功"""
    return success(data, message, ResponseCode.UPDATED)


def success_deleted(message: str = "删除成功"):
    """删除成功"""
    return success(None, message, ResponseCode.DELETED)


def error_unauthorized(message: str = None):
    """未授权"""
    return error(ResponseCode.UNAUTHORIZED, message)


def error_forbidden(message: str = None):
    """禁止访问"""
    return error(ResponseCode.FORBIDDEN, message)


def error_not_found(message: str = None):
    """资源不存在"""
    return error(ResponseCode.RESOURCE_NOT_FOUND, message)


def error_bad_request(message: str = None):
    """请求参数错误"""
    return error(ResponseCode.BAD_REQUEST, message)


def error_internal(message: str = None):
    """服务器内部错误"""
    return error(ResponseCode.INTERNAL_ERROR, message)


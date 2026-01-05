"""
自定义异常类
"""
from typing import Any, Optional
from fastapi import HTTPException
from app.core.codes import ResponseCode, ResponseMessage, get_http_status


class BusinessException(Exception):
    """业务异常基类"""
    
    def __init__(
        self,
        code: ResponseCode = ResponseCode.BUSINESS_ERROR,
        message: str = None,
        data: Any = None
    ):
        self.code = code
        self.message = message or ResponseMessage.get_message(code)
        self.data = data
        super().__init__(self.message)


class APIException(HTTPException):
    """API异常（继承自HTTPException，会被FastAPI自动处理）"""
    
    def __init__(
        self,
        code: ResponseCode = ResponseCode.INTERNAL_ERROR,
        message: str = None,
        data: Any = None
    ):
        self.code = code
        self.message = message or ResponseMessage.get_message(code)
        self.data = data
        super().__init__(
            status_code=get_http_status(code),
            detail=self.message
        )


# ===== 认证相关异常 =====
class UnauthorizedException(APIException):
    """未授权异常"""
    def __init__(self, message: str = None):
        super().__init__(ResponseCode.UNAUTHORIZED, message)


class TokenExpiredException(APIException):
    """Token过期异常"""
    def __init__(self, message: str = None):
        super().__init__(ResponseCode.TOKEN_EXPIRED, message)


class TokenInvalidException(APIException):
    """Token无效异常"""
    def __init__(self, message: str = None):
        super().__init__(ResponseCode.TOKEN_INVALID, message)


class PermissionDeniedException(APIException):
    """权限不足异常"""
    def __init__(self, message: str = None):
        super().__init__(ResponseCode.PERMISSION_DENIED, message)


# ===== 用户相关异常 =====
class UserNotFoundException(APIException):
    """用户不存在异常"""
    def __init__(self, message: str = None):
        super().__init__(ResponseCode.USER_NOT_FOUND, message)


class UserExistedException(APIException):
    """用户已存在异常"""
    def __init__(self, message: str = None):
        super().__init__(ResponseCode.USER_EXISTED, message)


class PhoneExistedException(APIException):
    """手机号已存在异常"""
    def __init__(self, message: str = None):
        super().__init__(ResponseCode.PHONE_EXISTED, message)


class EmailExistedException(APIException):
    """邮箱已存在异常"""
    def __init__(self, message: str = None):
        super().__init__(ResponseCode.EMAIL_EXISTED, message)


class WrongPasswordException(APIException):
    """密码错误异常"""
    def __init__(self, message: str = None):
        super().__init__(ResponseCode.WRONG_PASSWORD, message)


class UserBannedException(APIException):
    """用户被封禁异常"""
    def __init__(self, message: str = None):
        super().__init__(ResponseCode.USER_BANNED, message)


# ===== 资源相关异常 =====
class ResourceNotFoundException(APIException):
    """资源不存在异常"""
    def __init__(self, message: str = None):
        super().__init__(ResponseCode.RESOURCE_NOT_FOUND, message)


class ResourceExistedException(APIException):
    """资源已存在异常"""
    def __init__(self, message: str = None):
        super().__init__(ResponseCode.RESOURCE_EXISTED, message)


# ===== 识别服务异常 =====
class RecognitionFailedException(APIException):
    """识别失败异常"""
    def __init__(self, message: str = None):
        super().__init__(ResponseCode.RECOGNITION_FAILED, message)


class QuotaExceededException(APIException):
    """额度超限异常"""
    def __init__(self, message: str = None):
        super().__init__(ResponseCode.QUOTA_EXCEEDED, message)


class ImageFormatException(APIException):
    """图片格式错误异常"""
    def __init__(self, message: str = None):
        super().__init__(ResponseCode.IMAGE_FORMAT_ERROR, message)


# ===== 参数验证异常 =====
class ValidationException(APIException):
    """数据验证异常"""
    def __init__(self, message: str = None, data: Any = None):
        super().__init__(ResponseCode.VALIDATION_ERROR, message, data)


class ParameterException(APIException):
    """参数错误异常"""
    def __init__(self, message: str = None):
        super().__init__(ResponseCode.INVALID_PARAMETER, message)


# ===== 服务器异常 =====
class DatabaseException(APIException):
    """数据库异常"""
    def __init__(self, message: str = None):
        super().__init__(ResponseCode.DATABASE_ERROR, message)


class RedisException(APIException):
    """Redis异常"""
    def __init__(self, message: str = None):
        super().__init__(ResponseCode.REDIS_ERROR, message)


class InternalException(APIException):
    """内部错误异常"""
    def __init__(self, message: str = None):
        super().__init__(ResponseCode.INTERNAL_ERROR, message)


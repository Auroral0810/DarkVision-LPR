"""
统一业务状态码定义
采用 HTTP 状态码 + 业务状态码 的双重体系
"""
from enum import Enum


class ResponseCode(int, Enum):
    """统一响应状态码"""
    
    # ===== 成功类 (20000-20999) =====
    SUCCESS = 20000  # 操作成功
    CREATED = 20001  # 创建成功
    UPDATED = 20002  # 更新成功
    DELETED = 20003  # 删除成功
    
    # ===== 客户端错误类 (40000-49999) =====
    # 通用错误 (40000-40099)
    BAD_REQUEST = 40000  # 请求参数错误
    VALIDATION_ERROR = 40001  # 数据验证失败
    MISSING_PARAMETER = 40002  # 缺少必要参数
    INVALID_PARAMETER = 40003  # 参数格式错误
    
    # 认证授权错误 (40100-40199)
    UNAUTHORIZED = 40100  # 未登录/token失效
    TOKEN_EXPIRED = 40101  # token过期
    TOKEN_INVALID = 40102  # token无效
    FORBIDDEN = 40103  # 无权限访问
    LOGIN_REQUIRED = 40104  # 需要登录
    PERMISSION_DENIED = 40105  # 权限不足
    
    # 用户相关错误 (40200-40299)
    USER_NOT_FOUND = 40200  # 用户不存在
    USER_EXISTED = 40201  # 用户已存在
    PHONE_EXISTED = 40202  # 手机号已注册
    EMAIL_EXISTED = 40203  # 邮箱已注册
    NICKNAME_EXISTED = 40204  # 昵称已被使用
    WRONG_PASSWORD = 40205  # 密码错误
    USER_BANNED = 40206  # 用户已被封禁
    USER_INACTIVE = 40207  # 用户未激活
    OLD_PASSWORD_ERROR = 40208  # 原密码错误
    PASSWORD_NOT_MATCH = 40209  # 两次密码不一致
    
    # 资源相关错误 (40300-40399)
    RESOURCE_NOT_FOUND = 40300  # 资源不存在
    RESOURCE_EXISTED = 40301  # 资源已存在
    RESOURCE_DELETED = 40302  # 资源已删除
    
    # 识别服务错误 (40400-40499)
    RECOGNITION_FAILED = 40400  # 识别失败
    IMAGE_FORMAT_ERROR = 40401  # 图片格式错误
    IMAGE_SIZE_EXCEEDED = 40402  # 图片大小超限
    QUOTA_EXCEEDED = 40403  # 额度已用完
    NO_PLATE_DETECTED = 40404  # 未检测到车牌
    
    # 订单支付错误 (40500-40599)
    ORDER_NOT_FOUND = 40500  # 订单不存在
    ORDER_PAID = 40501  # 订单已支付
    ORDER_EXPIRED = 40502  # 订单已过期
    PAYMENT_FAILED = 40503  # 支付失败
    REFUND_FAILED = 40504  # 退款失败
    
    # 实名认证错误 (40600-40699)
    VERIFICATION_PENDING = 40600  # 认证审核中
    VERIFICATION_FAILED = 40601  # 认证失败
    VERIFICATION_REQUIRED = 40602  # 需要实名认证
    ID_CARD_INVALID = 40603  # 身份证信息无效
    
    # 频率限制错误 (40700-40799)
    RATE_LIMIT = 40700  # 请求过于频繁
    TOO_MANY_REQUESTS = 40701  # 请求次数超限
    
    # ===== 服务器错误类 (50000-59999) =====
    INTERNAL_ERROR = 50000  # 服务器内部错误
    DATABASE_ERROR = 50001  # 数据库错误
    REDIS_ERROR = 50002  # Redis错误
    THIRD_PARTY_ERROR = 50003  # 第三方服务错误
    FILE_UPLOAD_ERROR = 50004  # 文件上传失败
    AI_SERVICE_ERROR = 50005  # AI服务错误
    
    # ===== 业务错误类 (60000-69999) =====
    BUSINESS_ERROR = 60000  # 业务处理失败


class ResponseMessage:
    """响应消息映射"""
    
    messages = {
        # 成功
        ResponseCode.SUCCESS: "操作成功",
        ResponseCode.CREATED: "创建成功",
        ResponseCode.UPDATED: "更新成功",
        ResponseCode.DELETED: "删除成功",
        
        # 通用错误
        ResponseCode.BAD_REQUEST: "请求参数错误",
        ResponseCode.VALIDATION_ERROR: "数据验证失败",
        ResponseCode.MISSING_PARAMETER: "缺少必要参数",
        ResponseCode.INVALID_PARAMETER: "参数格式错误",
        
        # 认证授权
        ResponseCode.UNAUTHORIZED: "未登录或登录已过期",
        ResponseCode.TOKEN_EXPIRED: "登录已过期，请重新登录",
        ResponseCode.TOKEN_INVALID: "无效的访问令牌",
        ResponseCode.FORBIDDEN: "无权限访问",
        ResponseCode.LOGIN_REQUIRED: "请先登录",
        ResponseCode.PERMISSION_DENIED: "权限不足",
        
        # 用户相关
        ResponseCode.USER_NOT_FOUND: "用户不存在",
        ResponseCode.USER_EXISTED: "用户已存在",
        ResponseCode.PHONE_EXISTED: "手机号已被注册",
        ResponseCode.EMAIL_EXISTED: "邮箱已被注册",
        ResponseCode.NICKNAME_EXISTED: "昵称已被使用",
        ResponseCode.WRONG_PASSWORD: "手机号或密码错误",
        ResponseCode.USER_BANNED: "账户已被封禁",
        ResponseCode.USER_INACTIVE: "账户未激活",
        ResponseCode.OLD_PASSWORD_ERROR: "原密码错误",
        ResponseCode.PASSWORD_NOT_MATCH: "两次输入的密码不一致",
        
        # 资源相关
        ResponseCode.RESOURCE_NOT_FOUND: "资源不存在",
        ResponseCode.RESOURCE_EXISTED: "资源已存在",
        ResponseCode.RESOURCE_DELETED: "资源已被删除",
        
        # 识别服务
        ResponseCode.RECOGNITION_FAILED: "识别失败",
        ResponseCode.IMAGE_FORMAT_ERROR: "不支持的图片格式",
        ResponseCode.IMAGE_SIZE_EXCEEDED: "图片大小超过限制",
        ResponseCode.QUOTA_EXCEEDED: "今日识别次数已用完",
        ResponseCode.NO_PLATE_DETECTED: "未检测到车牌",
        
        # 订单支付
        ResponseCode.ORDER_NOT_FOUND: "订单不存在",
        ResponseCode.ORDER_PAID: "订单已支付",
        ResponseCode.ORDER_EXPIRED: "订单已过期",
        ResponseCode.PAYMENT_FAILED: "支付失败",
        ResponseCode.REFUND_FAILED: "退款失败",
        
        # 实名认证
        ResponseCode.VERIFICATION_PENDING: "认证审核中，请耐心等待",
        ResponseCode.VERIFICATION_FAILED: "实名认证失败",
        ResponseCode.VERIFICATION_REQUIRED: "需要先完成实名认证",
        ResponseCode.ID_CARD_INVALID: "身份证信息无效",
        
        # 频率限制
        ResponseCode.RATE_LIMIT: "请求过于频繁，请稍后再试",
        ResponseCode.TOO_MANY_REQUESTS: "请求次数超过限制",
        
        # 服务器错误
        ResponseCode.INTERNAL_ERROR: "服务器内部错误",
        ResponseCode.DATABASE_ERROR: "数据库错误",
        ResponseCode.REDIS_ERROR: "缓存服务错误",
        ResponseCode.THIRD_PARTY_ERROR: "第三方服务错误",
        ResponseCode.FILE_UPLOAD_ERROR: "文件上传失败",
        ResponseCode.AI_SERVICE_ERROR: "AI识别服务异常",
        
        # 业务错误
        ResponseCode.BUSINESS_ERROR: "业务处理失败",
    }
    
    @classmethod
    def get_message(cls, code: ResponseCode) -> str:
        """获取状态码对应的消息"""
        return cls.messages.get(code, "未知错误")


# HTTP 状态码映射
def get_http_status(code: ResponseCode) -> int:
    """将业务状态码映射到 HTTP 状态码"""
    if 20000 <= code < 21000:
        return 200  # 成功
    elif 40000 <= code < 41000:
        return 400  # 客户端错误
    elif 40100 <= code < 40200:
        return 401  # 未授权
    elif code == ResponseCode.FORBIDDEN or code == ResponseCode.PERMISSION_DENIED:
        return 403  # 禁止访问
    elif 40200 <= code < 50000:
        return 400  # 其他客户端错误
    elif 50000 <= code < 60000:
        return 500  # 服务器错误
    else:
        return 500  # 默认服务器错误


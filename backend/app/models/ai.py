from sqlalchemy import Column, String, Integer, Text, Boolean, DateTime, Float
from sqlalchemy.sql import func
from app.core.database import Base

class AiCommandRecord(Base):
    """
    AI 命令执行记录表
    """
    __tablename__ = "ai_command_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    
    # 原始请求
    original_command = Column(Text, nullable=False)
    current_route = Column(String(255))
    
    # 解析结果
    parse_success = Column(Boolean, default=False)
    provider = Column(String(50))  # 例如: openai, dashscope
    model = Column(String(50))     # 例如: qwen-max, gpt-4
    
    explanation = Column(Text)      # AI 的解释
    function_name = Column(String(100))
    function_arguments = Column(Text) # JSON 字符串
    confidence = Column(Float)
    
    # 执行状态
    execute_status = Column(String(20), default="pending") # pending, success, failed, revoked
    execute_result = Column(Text)
    execute_error_message = Column(Text)
    execution_time = Column(Float) # 执行耗时(秒)
    
    # 用户确认情况
    is_dangerous = Column(Boolean, default=False) # 是否高风险操作
    requires_confirmation = Column(Boolean, default=False)
    user_confirmed = Column(Boolean, default=False)
    
    # 统计信息
    input_tokens = Column(Integer, default=0)
    output_tokens = Column(Integer, default=0)
    total_tokens = Column(Integer, default=0)
    
    # 环境信息
    ip_address = Column(String(50))
    user_agent = Column(Text)
    
    create_time = Column(DateTime, server_default=func.now())
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now())
    remark = Column(String(255))

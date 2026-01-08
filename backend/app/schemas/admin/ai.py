from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class FunctionCallSchema(BaseModel):
    name: str = Field(..., description="函数名称")
    arguments: Dict[str, Any] = Field(..., description="参数对象")
    description: Optional[str] = None

class AiCommandRequest(BaseModel):
    command: str = Field(..., description="用户输入的自然语言命令")
    current_route: Optional[str] = None
    currentComponent: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class AiCommandResponse(BaseModel):
    parse_log_id: Optional[int] = None
    success: bool
    function_calls: List[FunctionCallSchema] = []
    explanation: Optional[str] = None
    confidence: Optional[float] = None
    error: Optional[str] = None

class AiExecuteRequest(BaseModel):
    parse_log_id: Optional[int] = None
    original_command: Optional[str] = None
    function_call: FunctionCallSchema
    confirm_mode: str = "manual" # auto, manual
    user_confirmed: bool = True
    current_route: Optional[str] = None

class AiExecuteResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    message: Optional[str] = None
    affected_rows: Optional[int] = None
    error: Optional[str] = None
    record_id: Optional[int] = None

class AiConfig(BaseModel):
    provider: str = Field("openai", description="AI 提供商 (openai/qwen/dashscope/gemini)")
    api_key: str = Field("", description="API Key")
    api_base: Optional[str] = Field(None, description="API Base URL")
    model: str = Field("gpt-3.5-turbo", description="模型名称")
    temperature: float = 0.7
    max_tokens: int = 2000
    enable_voice: bool = False
    enable_history: bool = True

class AiCommandRecordOut(BaseModel):
    id: int
    user_id: int = Field(..., serialization_alias="userId")
    username: Optional[str] = None
    original_command: str = Field(..., serialization_alias="originalCommand")
    current_route: Optional[str] = Field(None, serialization_alias="currentRoute")
    
    parse_success: bool = Field(..., serialization_alias="parseSuccess")
    provider: Optional[str] = None
    model: Optional[str] = None
    
    explanation: Optional[str] = None
    function_name: Optional[str] = Field(None, serialization_alias="functionName")
    function_arguments: Optional[str] = Field(None, serialization_alias="functionArguments")
    confidence: Optional[float] = None
    
    execute_status: str = Field(..., serialization_alias="executeStatus")
    execute_result: Optional[str] = Field(None, serialization_alias="executeResult")
    execute_error_message: Optional[str] = Field(None, serialization_alias="executeErrorMessage")
    execution_time: Optional[float] = Field(None, serialization_alias="executionTime")
    
    is_dangerous: bool = Field(False, serialization_alias="isDangerous")
    requires_confirmation: bool = Field(False, serialization_alias="requiresConfirmation")
    user_confirmed: bool = Field(False, serialization_alias="userConfirmed")
    
    input_tokens: int = Field(0, serialization_alias="inputTokens")
    output_tokens: int = Field(0, serialization_alias="outputTokens")
    total_tokens: int = Field(0, serialization_alias="totalTokens")
    
    ip_address: Optional[str] = Field(None, serialization_alias="ipAddress")
    user_agent: Optional[str] = Field(None, serialization_alias="userAgent")
    
    create_time: datetime = Field(..., serialization_alias="createTime")
    update_time: Optional[datetime] = Field(None, serialization_alias="updateTime")
    remark: Optional[str] = None
    
    class Config:
        from_attributes = True

class AiCommandRecordQuery(BaseModel):
    page_num: int = 1
    page_size: int = 10
    keywords: Optional[str] = None
    provider: Optional[str] = None
    model: Optional[str] = None
    parse_success: Optional[bool] = None
    execute_status: Optional[str] = None
    is_dangerous: Optional[bool] = None
    start_time: Optional[str] = None 
    end_time: Optional[str] = None
    createTime: Optional[List[str]] = Field(None)

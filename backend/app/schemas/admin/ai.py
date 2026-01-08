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

class AiCommandRecordOut(BaseModel):
    id: int
    user_id: int
    original_command: str
    parse_success: bool
    function_name: Optional[str] = None
    execute_status: str
    create_time: datetime
    
    class Config:
        from_attributes = True

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Any
from app.core.database import get_db
from app.api import deps
from app.schemas.admin.ai import AiCommandRequest, AiCommandResponse, AiExecuteRequest, AiExecuteResponse, AiConfig, AiCommandRecordQuery
from app.services.admin.ai_service import AiService
from app.core.response import success_response, UnifiedResponse

router = APIRouter()

@router.post("/command/parse", response_model=UnifiedResponse)
async def parse_ai_command(
    request: AiCommandRequest,
    db: Session = Depends(get_db),
    current_admin = Depends(deps.get_current_active_admin)
):
    """
    解析自然语言命令
    """
    result = await AiService.parse_command(db, current_admin.id, request)
    return success_response(data=result)

@router.post("/command/execute", response_model=UnifiedResponse)
async def execute_ai_command(
    request: AiExecuteRequest,
    db: Session = Depends(get_db),
    current_admin = Depends(deps.get_current_active_admin)
):
    """
    执行 AI 命令
    """
    try:
        result = await AiService.execute_command(db, current_admin.id, request)
        return success_response(data=AiExecuteResponse(
            success=True,
            data=result,
            message="操作执行成功",
            error=None
        ))
    except Exception as e:
        return success_response(data=AiExecuteResponse(
            success=False,
            error=str(e),
            message="操作执行失败"
        ))

@router.post("/command/records", response_model=UnifiedResponse)
async def get_command_records(
    query: AiCommandRecordQuery,
    db: Session = Depends(get_db),
    current_admin = Depends(deps.get_current_active_admin)
):
    """
    获取 AI 命令记录列表
    """
    result = AiService.get_record_page(db, query)
    return success_response(data=result)

@router.get("/command/records", response_model=UnifiedResponse)
async def get_command_records_get_method(
    page_num: int = 1,
    page_size: int = 10,
    keywords: str = None,
    db: Session = Depends(get_db),
    current_admin = Depends(deps.get_current_active_admin)
):
    """
    获取 AI 命令记录列表 (GET 方式支持)
    """
    query = AiCommandRecordQuery(
        page_num=page_num,
        page_size=page_size,
        keywords=keywords
    )
    result = AiService.get_record_page(db, query)
    return success_response(data=result)

@router.get("/config", response_model=UnifiedResponse)
async def get_ai_config(
    db: Session = Depends(get_db),
    current_admin = Depends(deps.get_current_active_admin)
):
    """
    获取 AI 配置
    """
    result = AiService.get_config(db)
    return success_response(data=result)

@router.post("/config", response_model=UnifiedResponse)
async def update_ai_config(
    config: AiConfig,
    db: Session = Depends(get_db),
    current_admin = Depends(deps.get_current_active_admin)
):
    """
    更新 AI 配置
    """
    AiService.save_config(db, config)
    return success_response(data=config)

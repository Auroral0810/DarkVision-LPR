from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Any
from app.core.database import get_db
from app.api import deps
from app.schemas.admin.ai import AiCommandRequest, AiCommandResponse, AiExecuteRequest, AiExecuteResponse, AiConfig, AiCommandRecordQuery
from app.services.admin.ai_service import AiService
from app.core.response import UnifiedResponse

router = APIRouter()

@router.get("/config", response_model=UnifiedResponse[AiConfig])
def get_ai_config(
    db: Session = Depends(get_db),
    current_admin = Depends(deps.get_current_active_admin)
):
    """获取AI配置"""
    config = AiService.get_config(db)
    return UnifiedResponse.success(config)

@router.put("/config", response_model=UnifiedResponse)
def update_ai_config(
    config: AiConfig,
    db: Session = Depends(get_db),
    current_admin = Depends(deps.get_current_active_admin)
):
    """更新AI配置"""
    AiService.save_config(db, config)
    return UnifiedResponse.success()

@router.post("/record/page", response_model=UnifiedResponse)
def get_ai_record_page(
    query: AiCommandRecordQuery,
    db: Session = Depends(get_db),
    current_admin = Depends(deps.get_current_active_admin)
):
    """获取AI命令记录分页"""
    data = AiService.get_record_page(db, query)
    return UnifiedResponse.success(data)

@router.post("/command/parse", response_model=AiCommandResponse)
async def parse_ai_command(
    request: AiCommandRequest,
    db: Session = Depends(get_db),
    current_admin = Depends(deps.get_current_active_admin)
):
    """
    解析自然语言命令
    """
    return await AiService.parse_command(db, current_admin.id, request)

@router.post("/command/execute", response_model=AiExecuteResponse)
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
        return AiExecuteResponse(
            success=True,
            data=result,
            message="操作执行成功"
        )
    except Exception as e:
        return AiExecuteResponse(
            success=False,
            error=str(e),
            message="操作执行失败"
        )

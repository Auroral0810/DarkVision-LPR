from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Any
from app.core.database import get_db
from app.api import deps
from app.schemas.admin.ai import AiCommandRequest, AiCommandResponse, AiExecuteRequest, AiExecuteResponse
from app.services.admin.ai_service import AiService

router = APIRouter()

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

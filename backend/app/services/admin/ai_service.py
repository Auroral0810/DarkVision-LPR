import json
import logging
import time
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.ai import AiCommandRecord
from app.models.user import User
from app.schemas.admin.ai import AiCommandRequest, AiCommandResponse, AiExecuteRequest, FunctionCallSchema, AiConfig, AiCommandRecordQuery, AiCommandRecordOut
from app.config import settings
from app.services.admin.system_service import system_service
from datetime import datetime

logger = logging.getLogger(__name__)

class AiService:
    @staticmethod
    def get_config(db: Session) -> AiConfig:
        """获取AI配置"""
        configs = system_service.get_configs_by_prefix(db, "ai.")
        if not configs:
            return AiConfig()
        return AiConfig(**configs)

    @staticmethod
    def save_config(db: Session, config: AiConfig):
        """保存AI配置"""
        config_dict = config.model_dump()
        prefixed_dict = {f"ai.{k}": v for k, v in config_dict.items()}
        system_service.update_configs(db, prefixed_dict)

    @staticmethod
    def get_record_page(db: Session, query: AiCommandRecordQuery) -> Dict[str, Any]:
        """分页获取命令记录"""
        q = db.query(AiCommandRecord)
        
        if query.keywords:
            q = q.filter(
                (AiCommandRecord.original_command.ilike(f"%{query.keywords}%")) |
                (AiCommandRecord.function_name.ilike(f"%{query.keywords}%"))
            )
        
        if query.provider:
            q = q.filter(AiCommandRecord.provider == query.provider)
            
        if query.model:
            q = q.filter(AiCommandRecord.model.ilike(f"%{query.model}%"))
            
        if query.parse_success is not None:
            q = q.filter(AiCommandRecord.parse_success == query.parse_success)
            
        if query.execute_status:
            q = q.filter(AiCommandRecord.execute_status == query.execute_status)
            
        if query.is_dangerous is not None:
            q = q.filter(AiCommandRecord.is_dangerous == query.is_dangerous)
            
        if query.start_time:
            q = q.filter(AiCommandRecord.create_time >= query.start_time)
        if query.end_time:
            q = q.filter(AiCommandRecord.create_time <= query.end_time)

        # Handle frontend createTime array
        if query.createTime and len(query.createTime) == 2:
            start_str, end_str = query.createTime
            if start_str:
                q = q.filter(AiCommandRecord.create_time >= start_str)
            if end_str:
                # Assuming date only, append end of day time
                if len(end_str) == 10: # YYYY-MM-DD
                    end_str += " 23:59:59"
                q = q.filter(AiCommandRecord.create_time <= end_str)

        total = q.count()
        
        # 分页
        records = q.order_by(desc(AiCommandRecord.create_time)) \
            .offset((query.page_num - 1) * query.page_size) \
            .limit(query.page_size) \
            .all()

        # 填充用户名
        user_ids = list(set(r.user_id for r in records))
        users = db.query(User).filter(User.id.in_(user_ids)).all()
        user_map = {u.id: u.nickname for u in users}
        
        result_list = []
        for r in records:
            # Pydantic 转换
            item = AiCommandRecordOut.model_validate(r)
            item.username = user_map.get(r.user_id, str(r.user_id))
            result_list.append(item)
            
        return {
            "list": result_list,
            "total": total,
            "page_num": query.page_num,
            "page_size": query.page_size
        }

    @staticmethod
    async def parse_command(db: Session, user_id: int, request: AiCommandRequest) -> AiCommandResponse:
        """
        解析自然语音命令为结构化函数调用
        """
        config = AiService.get_config(db)
        
        # 记录初始日志
        record = AiCommandRecord(
            user_id=user_id,
            original_command=request.command,
            current_route=request.current_route,
            execute_status="pending",
            provider=config.provider, 
            model=config.model
        )
        db.add(record)
        db.commit()
        db.refresh(record)

        # 这里应该调用 LLM (OpenAI/DashScope)
        # 暂时模拟解析逻辑或占位，实际需要集成 SDK
        
        # 演示用：硬编码一些常见的命令解析
        cmd = request.command.lower()
        functions = []
        explanation = ""
        
        if "用户" in cmd and ("管理" in cmd or "列表" in cmd):
            explanation = "正在为您前往用户管理页面"
            # 这是一个纯跳转指令，由前端根据解释推断，或者返回一个特定的 navigate 函数
        elif "修改" in cmd and "密码" in cmd:
            explanation = "准备为您修改用户密码"
            functions.append(FunctionCallSchema(
                name="updateUserPassword",
                arguments={"username": "test", "newPassword": "..."}
            ))
            record.is_dangerous = True
        else:
            explanation = f"我理解您想：{request.command}。但我还在学习如何更准确地执行这个操作。"

        # 更新记录
        record.parse_success = True
        record.explanation = explanation
        if functions:
            record.function_name = functions[0].name
            record.function_arguments = json.dumps([f.model_dump() for f in functions]) if functions else None
            # 注意：前端可能期望 function_arguments 是 JSON 字符串
            # 这里的 functions[0].arguments 是 dict，需要 dump
            if len(functions) > 0:
                record.function_arguments = json.dumps(functions[0].arguments)
        
        db.commit()

        return AiCommandResponse(
            parse_log_id=record.id,
            success=True,
            function_calls=functions,
            explanation=explanation,
            confidence=0.9
        )

    @staticmethod
    async def execute_command(db: Session, user_id: int, request: AiExecuteRequest) -> Dict[str, Any]:
        """
        执行已解析的函数调用
        """
        start_time = time.time()
        
        # 1. 查找解析记录
        record = None
        if request.parse_log_id:
            record = db.query(AiCommandRecord).filter(AiCommandRecord.id == request.parse_log_id).first()

        # 2. 权限校验 (略)
        
        # 3. 动态执行逻辑
        fn_name = request.function_call.name
        
        result_data = {"status": "success", "message": f"成功执行了 {fn_name}"}
        
        # 更新记录状态
        if record:
            record.execute_status = "success"
            record.execute_result = json.dumps(result_data)
            record.execution_time = time.time() - start_time
            # record.user_confirmed = request.user_confirmed # if passed
            db.commit()
            
        return result_data

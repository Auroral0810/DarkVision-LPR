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
                arguments={"username": "test", "newPassword": "123456(示例)"}
            ))
            record.is_dangerous = True
            
        # --- Heuristic Rules for Full CRUD Support (Demo Mode) ---
        elif "创建用户" in cmd or "添加用户" in cmd:
            # 简单提取：创建用户 手机号 13800000000 密码 123456
            explanation = "准备为您创建新用户"
            # 模拟参数提取
            functions.append(FunctionCallSchema(
                name="createUser",
                arguments={"phone": "13800000000", "password": "password123", "nickname": "AI创建用户"}
            ))
            record.is_dangerous = True

        elif "发布公告" in cmd:
            explanation = "准备发布新公告"
            functions.append(FunctionCallSchema(
                name="createAnnouncement",
                arguments={"title": "AI 自动发布公告", "content": "这是一条由 AI 助手发布的测试公告", "type": "info"}
            ))
            
        elif "封禁" in cmd or "禁用" in cmd:
            explanation = "准备封禁用户"
            functions.append(FunctionCallSchema(
                name="banUser",
                arguments={"user_id": 1, "reason": "违规操作(AI检测)", "duration_days": 3}
            ))
            record.is_dangerous = True
            
        elif "黑名单" in cmd and "ip" in cmd:
            explanation = "准备添加 IP 黑名单"
            functions.append(FunctionCallSchema(
                name="addIpRule",
                arguments={"ip": "192.168.1.100", "type": "deny", "remark": "AI 自动拦截"}
            ))
            
        elif "创建角色" in cmd:
            explanation = "准备创建新角色"
            functions.append(FunctionCallSchema(
                name="createRole",
                arguments={"name": "新角色", "description": "AI 创建的角色", "permission_ids": []}
            ))

        elif "创建套餐" in cmd:
            explanation = "准备创建新套餐"
            functions.append(FunctionCallSchema(
                name="createPackage",
                arguments={"name": "AI特惠包", "code": "ai_pkg_001", "price": 99.9, "duration_months": 1, "description": "AI生成的测试套餐"}
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

        # 2. 权限校验 (略 - 在 Dispatcher 或 Service 层处理)
        
        # 3. 动态执行逻辑
        fn_name = request.function_call.name
        args = request.function_call.arguments
        
        try:
            # 使用分发器执行
            from app.services.admin.ai_functions import AiDispatcher
            result_payload = await AiDispatcher.dispatch(db, user_id, fn_name, args)
            
            result_data = {
                "status": "success", 
                "message": result_payload.get("message", "操作执行成功"),
                "data": result_payload
            }
            execute_status = "success"
            error_msg = None
            
        except Exception as e:
            logger.error(f"AI Execute Error: {e}", exc_info=True)
            result_data = {"status": "error", "message": str(e)}
            execute_status = "failed"
            error_msg = str(e)
        
        # 4. 更新记录状态
        if record:
            record.execute_status = execute_status
            record.execute_result = json.dumps(result_data, ensure_ascii=False)
            record.execution_time = time.time() - start_time
            if error_msg:
                record.execute_error_message = error_msg
            # record.user_confirmed = request.user_confirmed # if passed
            db.commit()
            
        if execute_status == "failed":
            raise Exception(error_msg)
            
        return result_data

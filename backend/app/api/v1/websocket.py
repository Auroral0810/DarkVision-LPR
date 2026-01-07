from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.websocket_manager import manager

router = APIRouter()

@router.websocket("/ws/{task_uuid}")
async def websocket_endpoint(websocket: WebSocket, task_uuid: str):
    await manager.connect(task_uuid, websocket)
    try:
        while True:
            # Keep connection alive, maybe receive commands (e.g., cancel)
            data = await websocket.receive_text()
            # For now, we just echo or ignore client messages
            # await manager.send_personal_message(f"You wrote: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(task_uuid, websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(task_uuid, websocket)

@router.websocket("/ws/user/{user_id}")
async def websocket_user_endpoint(websocket: WebSocket, user_id: int, token: str = None):
    # 简单的 Token 校验
    from app.core.security import decode_access_token
    
    if not token:
        await websocket.close(code=1008)
        return

    payload = decode_access_token(token)
    if not payload or payload.get("user_id") != user_id:
        await websocket.close(code=1008)
        return

    await manager.connect_user(user_id, websocket)
    try:
        while True:
            await websocket.receive_text()
            # 保持连接活跃，忽略客户端消息
    except WebSocketDisconnect:
        manager.disconnect_user(user_id, websocket)
    except Exception as e:
        print(f"User WebSocket error: {e}")
        manager.disconnect_user(user_id, websocket)

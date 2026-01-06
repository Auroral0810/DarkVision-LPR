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


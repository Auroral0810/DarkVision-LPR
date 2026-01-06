from typing import Dict, List
from fastapi import WebSocket
import logging

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        # Store active connections: task_id -> List[WebSocket]
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, task_uuid: str, websocket: WebSocket):
        await websocket.accept()
        if task_uuid not in self.active_connections:
            self.active_connections[task_uuid] = []
        self.active_connections[task_uuid].append(websocket)
        logger.info(f"WebSocket connected for task {task_uuid}. Total connections: {len(self.active_connections[task_uuid])}")

    def disconnect(self, task_uuid: str, websocket: WebSocket):
        if task_uuid in self.active_connections:
            if websocket in self.active_connections[task_uuid]:
                self.active_connections[task_uuid].remove(websocket)
            if not self.active_connections[task_uuid]:
                del self.active_connections[task_uuid]
        logger.info(f"WebSocket disconnected for task {task_uuid}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast_to_task(self, task_uuid: str, message: dict):
        logger.info(f"Broadcasting to task {task_uuid}: {message.get('type')} - {message.get('status')}")
        if task_uuid in self.active_connections:
            for connection in self.active_connections[task_uuid]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"Error sending message to websocket: {e}")
                    # Could choose to disconnect here if broken
        else:
            logger.warning(f"No active WebSocket connections for task {task_uuid}")

manager = ConnectionManager()

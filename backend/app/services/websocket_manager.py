from typing import Dict, List
from fastapi import WebSocket
import logging

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        # Store active connections: task_id -> List[WebSocket]
        self.active_connections: Dict[str, List[WebSocket]] = {}
        # Store active user connections: user_id -> List[WebSocket]
        self.active_user_connections: Dict[int, List[WebSocket]] = {}

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

    async def connect_user(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        if user_id not in self.active_user_connections:
            self.active_user_connections[user_id] = []
        self.active_user_connections[user_id].append(websocket)
        logger.info(f"User {user_id} connected to WebSocket. Total connections: {len(self.active_user_connections[user_id])}")

    def disconnect_user(self, user_id: int, websocket: WebSocket):
        if user_id in self.active_user_connections:
            if websocket in self.active_user_connections[user_id]:
                self.active_user_connections[user_id].remove(websocket)
            if not self.active_user_connections[user_id]:
                del self.active_user_connections[user_id]
        logger.info(f"User {user_id} disconnected from WebSocket")

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
        else:
            logger.warning(f"No active WebSocket connections for task {task_uuid}")

    async def broadcast_to_user(self, user_id: int, message: dict):
        """
        向指定用户发送消息（支持多端登录）
        """
        logger.info(f"Broadcasting to user {user_id}: {message}")
        if user_id in self.active_user_connections:
            for connection in self.active_user_connections[user_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"Error sending message to user {user_id}: {e}")
                    # Remove broken connection?
        else:
            logger.debug(f"User {user_id} is not connected via WebSocket")

manager = ConnectionManager()

"""
WebSocket 管理器
管理 WebSocket 連接和訊息廣播
"""

from typing import List, Dict
from fastapi import WebSocket
from notification_interface import INotificationService
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConnectionManager:
    """WebSocket 連接管理器 - 負責管理 WebSocket 連接"""

    def __init__(self):
        """初始化連接管理器"""
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        """接受新的 WebSocket 連接"""
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"新連接已建立。目前連接數: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket) -> None:
        """移除 WebSocket 連接"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"連接已中斷。目前連接數: {len(self.active_connections)}")

    async def send_personal_message(self, message: str, websocket: WebSocket) -> None:
        """發送個人訊息"""
        try:
            await websocket.send_text(message)
        except Exception as e:
            logger.error(f"發送個人訊息時發生錯誤: {e}")
            self.disconnect(websocket)

    async def broadcast(self, message: dict) -> None:
        """廣播訊息給所有連接的客戶端"""
        message_str = json.dumps(message, ensure_ascii=False, default=str)
        logger.info(f"廣播訊息給 {len(self.active_connections)} 個連接: {message_str}")
        
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message_str)
            except Exception as e:
                logger.error(f"廣播訊息時發生錯誤: {e}")
                disconnected.append(connection)
        
        # 移除斷開的連接
        for connection in disconnected:
            self.disconnect(connection)


class WebSocketNotificationService(INotificationService):
    """
    WebSocket 通知服務 - 實作通知介面
    符合單一職責原則 (SRP) 和依賴反轉原則 (DIP)
    """

    def __init__(self, connection_manager: ConnectionManager):
        """初始化通知服務"""
        self.connection_manager = connection_manager

    async def notify(self, message: Dict) -> None:
        """透過 WebSocket 發送通知"""
        await self.connection_manager.broadcast(message)


# 全域實例
manager = ConnectionManager()
websocket_notification_service = WebSocketNotificationService(manager)

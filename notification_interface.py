"""
通知介面
定義通知服務的抽象介面，符合依賴反轉原則 (DIP)
"""

from abc import ABC, abstractmethod
from typing import Dict


class INotificationService(ABC):
    """通知服務介面"""

    @abstractmethod
    async def notify(self, message: Dict) -> None:
        """
        發送通知
        
        Args:
            message: 要發送的訊息字典
        """
        pass


class ITaskRepository(ABC):
    """任務儲存庫介面"""

    @abstractmethod
    def save(self, task) -> None:
        """儲存任務"""
        pass

    @abstractmethod
    def find_by_id(self, task_id: str):
        """根據 ID 查詢任務"""
        pass

    @abstractmethod
    def find_all(self):
        """查詢所有任務"""
        pass

    @abstractmethod
    def delete(self, task_id: str) -> bool:
        """刪除任務"""
        pass

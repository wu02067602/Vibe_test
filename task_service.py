"""
Task 服務
管理任務的 CRUD 操作和狀態通知
符合 SOLID 原則的設計
"""

from typing import Dict, List, Optional
from task_model import Task, TaskStatus, TaskNotification
from notification_interface import INotificationService, ITaskRepository
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InMemoryTaskRepository(ITaskRepository):
    """
    記憶體任務儲存庫 - 實作任務儲存介面
    符合單一職責原則 (SRP) 和依賴反轉原則 (DIP)
    """

    def __init__(self):
        """初始化儲存庫"""
        self._tasks: Dict[str, Task] = {}

    def save(self, task: Task) -> None:
        """儲存任務"""
        self._tasks[task.id] = task
        logger.info(f"儲存任務: {task.id} - {task.title}")

    def find_by_id(self, task_id: str) -> Optional[Task]:
        """根據 ID 查詢任務"""
        return self._tasks.get(task_id)

    def find_all(self) -> List[Task]:
        """查詢所有任務"""
        return list(self._tasks.values())

    def delete(self, task_id: str) -> bool:
        """刪除任務"""
        if task_id in self._tasks:
            del self._tasks[task_id]
            logger.info(f"刪除任務: {task_id}")
            return True
        return False


class TaskService:
    """
    任務服務類別 - 負責任務管理業務邏輯
    符合單一職責原則 (SRP) 和依賴反轉原則 (DIP)
    依賴抽象介面而非具體實作
    """

    def __init__(
        self, 
        repository: ITaskRepository,
        notification_service: INotificationService
    ):
        """
        初始化任務服務
        
        Args:
            repository: 任務儲存庫介面
            notification_service: 通知服務介面
        """
        self.repository = repository
        self.notification_service = notification_service

    def create_task(self, task: Task) -> Task:
        """建立新任務"""
        self.repository.save(task)
        return task

    def get_task(self, task_id: str) -> Optional[Task]:
        """取得指定任務"""
        return self.repository.find_by_id(task_id)

    def get_all_tasks(self) -> List[Task]:
        """取得所有任務"""
        return self.repository.find_all()

    def delete_task(self, task_id: str) -> bool:
        """刪除任務"""
        return self.repository.delete(task_id)

    async def update_task_status(self, task_id: str, new_status: TaskStatus) -> Optional[Task]:
        """
        更新任務狀態並透過通知服務發送通知
        
        當任務狀態為 TO DO, IN PROGRESS, DONE 時，自動通知所有訂閱者
        """
        task = self.get_task(task_id)
        if not task:
            logger.warning(f"任務不存在: {task_id}")
            return None

        old_status = task.task_type
        task.update_status(new_status)
        self.repository.save(task)
        
        # 建立通知訊息
        notification = TaskNotification(
            task_id=task.id,
            title=task.title,
            old_status=old_status,
            new_status=new_status,
            message=f"任務「{task.title}」狀態已從「{old_status}」變更為「{new_status}」"
        )

        # 透過通知服務發送通知（依賴抽象介面）
        await self.notification_service.notify({
            "type": "task_status_update",
            "data": notification.model_dump()
        })

        logger.info(f"任務狀態已更新: {task_id} - {old_status} → {new_status}")
        return task


# 全域實例 - 使用依賴注入
from websocket_manager import websocket_notification_service

task_repository = InMemoryTaskRepository()
task_service = TaskService(
    repository=task_repository,
    notification_service=websocket_notification_service
)

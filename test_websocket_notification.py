"""
WebSocket 通知功能單元測試
測試任務狀態變更時的 WebSocket 通知功能
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from task_model import Task, TaskStatus, TaskNotification
from task_service import TaskService, InMemoryTaskRepository
from notification_interface import INotificationService


class MockNotificationService(INotificationService):
    """模擬通知服務，用於測試"""

    def __init__(self):
        self.notifications = []
        self.notify_called = False

    async def notify(self, message):
        """記錄通知訊息"""
        self.notifications.append(message)
        self.notify_called = True


class TestWebSocketNotification:
    """WebSocket 通知功能測試類別"""

    def setup_method(self):
        """測試前的準備工作"""
        self.repository = InMemoryTaskRepository()
        self.notification_service = MockNotificationService()
        self.task_service = TaskService(
            repository=self.repository,
            notification_service=self.notification_service
        )

    def test_create_task(self):
        """測試建立任務"""
        # Arrange: 準備測試資料
        task = Task(
            id="task-1",
            title="測試任務",
            description="這是一個測試任務",
            task_type=TaskStatus.TODO
        )

        # Act: 執行測試
        created_task = self.task_service.create_task(task)

        # Assert: 驗證結果
        assert created_task.id == "task-1"
        assert created_task.title == "測試任務"
        assert created_task.task_type == TaskStatus.TODO

        # 驗證任務已儲存
        saved_task = self.task_service.get_task("task-1")
        assert saved_task is not None
        assert saved_task.id == "task-1"

    @pytest.mark.asyncio
    async def test_update_task_status_to_in_progress(self):
        """測試將任務狀態更新為 IN PROGRESS 時發送通知"""
        # Arrange: 建立初始任務
        task = Task(
            id="task-2",
            title="進行中的任務",
            description="測試 IN PROGRESS 狀態",
            task_type=TaskStatus.TODO
        )
        self.task_service.create_task(task)

        # Act: 更新任務狀態為 IN PROGRESS
        updated_task = await self.task_service.update_task_status(
            "task-2", 
            TaskStatus.IN_PROGRESS
        )

        # Assert: 驗證任務狀態已更新
        assert updated_task is not None
        assert updated_task.task_type == TaskStatus.IN_PROGRESS

        # 驗證通知已發送
        assert self.notification_service.notify_called
        assert len(self.notification_service.notifications) == 1

        # 驗證通知內容
        notification = self.notification_service.notifications[0]
        assert notification["type"] == "task_status_update"
        assert notification["data"]["task_id"] == "task-2"
        assert notification["data"]["old_status"] == TaskStatus.TODO
        assert notification["data"]["new_status"] == TaskStatus.IN_PROGRESS

    @pytest.mark.asyncio
    async def test_update_task_status_to_done(self):
        """測試將任務狀態更新為 DONE 時發送通知"""
        # Arrange: 建立初始任務
        task = Task(
            id="task-3",
            title="完成的任務",
            description="測試 DONE 狀態",
            task_type=TaskStatus.IN_PROGRESS
        )
        self.task_service.create_task(task)

        # Act: 更新任務狀態為 DONE
        updated_task = await self.task_service.update_task_status(
            "task-3", 
            TaskStatus.DONE
        )

        # Assert: 驗證任務狀態已更新
        assert updated_task is not None
        assert updated_task.task_type == TaskStatus.DONE

        # 驗證通知已發送
        assert self.notification_service.notify_called
        assert len(self.notification_service.notifications) == 1

        # 驗證通知內容
        notification = self.notification_service.notifications[0]
        assert notification["type"] == "task_status_update"
        assert notification["data"]["task_id"] == "task-3"
        assert notification["data"]["old_status"] == TaskStatus.IN_PROGRESS
        assert notification["data"]["new_status"] == TaskStatus.DONE

    @pytest.mark.asyncio
    async def test_update_task_status_to_todo(self):
        """測試將任務狀態更新為 TO DO 時發送通知"""
        # Arrange: 建立初始任務
        task = Task(
            id="task-4",
            title="重置的任務",
            description="測試 TO DO 狀態",
            task_type=TaskStatus.IN_PROGRESS
        )
        self.task_service.create_task(task)

        # Act: 更新任務狀態為 TO DO
        updated_task = await self.task_service.update_task_status(
            "task-4", 
            TaskStatus.TODO
        )

        # Assert: 驗證任務狀態已更新
        assert updated_task is not None
        assert updated_task.task_type == TaskStatus.TODO

        # 驗證通知已發送
        assert self.notification_service.notify_called
        assert len(self.notification_service.notifications) == 1

        # 驗證通知內容
        notification = self.notification_service.notifications[0]
        assert notification["type"] == "task_status_update"
        assert notification["data"]["task_id"] == "task-4"
        assert notification["data"]["old_status"] == TaskStatus.IN_PROGRESS
        assert notification["data"]["new_status"] == TaskStatus.TODO

    @pytest.mark.asyncio
    async def test_multiple_status_updates(self):
        """測試多次狀態更新都會發送通知"""
        # Arrange: 建立初始任務
        task = Task(
            id="task-5",
            title="多狀態任務",
            description="測試多次狀態變更",
            task_type=TaskStatus.TODO
        )
        self.task_service.create_task(task)

        # Act: 執行多次狀態更新
        await self.task_service.update_task_status("task-5", TaskStatus.IN_PROGRESS)
        await self.task_service.update_task_status("task-5", TaskStatus.DONE)
        await self.task_service.update_task_status("task-5", TaskStatus.TODO)

        # Assert: 驗證所有通知都已發送
        assert len(self.notification_service.notifications) == 3

        # 驗證第一次通知
        assert self.notification_service.notifications[0]["data"]["old_status"] == TaskStatus.TODO
        assert self.notification_service.notifications[0]["data"]["new_status"] == TaskStatus.IN_PROGRESS

        # 驗證第二次通知
        assert self.notification_service.notifications[1]["data"]["old_status"] == TaskStatus.IN_PROGRESS
        assert self.notification_service.notifications[1]["data"]["new_status"] == TaskStatus.DONE

        # 驗證第三次通知
        assert self.notification_service.notifications[2]["data"]["old_status"] == TaskStatus.DONE
        assert self.notification_service.notifications[2]["data"]["new_status"] == TaskStatus.TODO

    @pytest.mark.asyncio
    async def test_update_nonexistent_task(self):
        """測試更新不存在的任務"""
        # Act: 嘗試更新不存在的任務
        result = await self.task_service.update_task_status(
            "nonexistent-task", 
            TaskStatus.DONE
        )

        # Assert: 驗證返回 None
        assert result is None

        # 驗證沒有發送通知
        assert not self.notification_service.notify_called
        assert len(self.notification_service.notifications) == 0

    def test_get_all_tasks(self):
        """測試取得所有任務"""
        # Arrange: 建立多個任務
        tasks = [
            Task(id="task-6", title="任務 1", task_type=TaskStatus.TODO),
            Task(id="task-7", title="任務 2", task_type=TaskStatus.IN_PROGRESS),
            Task(id="task-8", title="任務 3", task_type=TaskStatus.DONE),
        ]

        for task in tasks:
            self.task_service.create_task(task)

        # Act: 取得所有任務
        all_tasks = self.task_service.get_all_tasks()

        # Assert: 驗證任務數量
        assert len(all_tasks) == 3

        # 驗證每個任務都存在
        task_ids = [task.id for task in all_tasks]
        assert "task-6" in task_ids
        assert "task-7" in task_ids
        assert "task-8" in task_ids

    def test_delete_task(self):
        """測試刪除任務"""
        # Arrange: 建立任務
        task = Task(
            id="task-9",
            title="待刪除的任務",
            task_type=TaskStatus.TODO
        )
        self.task_service.create_task(task)

        # 驗證任務存在
        assert self.task_service.get_task("task-9") is not None

        # Act: 刪除任務
        result = self.task_service.delete_task("task-9")

        # Assert: 驗證刪除成功
        assert result is True
        assert self.task_service.get_task("task-9") is None

    def test_delete_nonexistent_task(self):
        """測試刪除不存在的任務"""
        # Act: 嘗試刪除不存在的任務
        result = self.task_service.delete_task("nonexistent-task")

        # Assert: 驗證刪除失敗
        assert result is False

    @pytest.mark.asyncio
    async def test_notification_message_format(self):
        """測試通知訊息格式是否正確"""
        # Arrange: 建立任務
        task = Task(
            id="task-10",
            title="格式測試任務",
            description="測試通知訊息格式",
            task_type=TaskStatus.TODO
        )
        self.task_service.create_task(task)

        # Act: 更新任務狀態
        await self.task_service.update_task_status("task-10", TaskStatus.IN_PROGRESS)

        # Assert: 驗證通知訊息格式
        notification = self.notification_service.notifications[0]
        
        assert "type" in notification
        assert "data" in notification
        
        data = notification["data"]
        assert "task_id" in data
        assert "title" in data
        assert "old_status" in data
        assert "new_status" in data
        assert "timestamp" in data
        assert "message" in data
        
        # 驗證訊息內容
        assert data["task_id"] == "task-10"
        assert data["title"] == "格式測試任務"
        assert "已從" in data["message"]
        assert "變更為" in data["message"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

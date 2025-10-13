"""
Task 模型
定義任務的資料結構和狀態
"""

from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class TaskStatus(str, Enum):
    """任務狀態枚舉"""
    TODO = "TO DO"
    IN_PROGRESS = "IN PROGRESS"
    DONE = "DONE"


class Task(BaseModel):
    """任務模型"""
    model_config = ConfigDict(use_enum_values=True)
    
    id: str = Field(..., description="任務唯一識別碼")
    title: str = Field(..., description="任務標題")
    description: Optional[str] = Field(None, description="任務描述")
    task_type: TaskStatus = Field(TaskStatus.TODO, description="任務狀態類型")
    created_at: datetime = Field(default_factory=datetime.now, description="建立時間")
    updated_at: datetime = Field(default_factory=datetime.now, description="更新時間")

    def update_status(self, new_status: TaskStatus) -> None:
        """更新任務狀態"""
        self.task_type = new_status
        self.updated_at = datetime.now()


class TaskNotification(BaseModel):
    """任務通知模型"""
    model_config = ConfigDict(use_enum_values=True)
    
    task_id: str = Field(..., description="任務 ID")
    title: str = Field(..., description="任務標題")
    old_status: Optional[TaskStatus] = Field(None, description="舊狀態")
    new_status: TaskStatus = Field(..., description="新狀態")
    timestamp: datetime = Field(default_factory=datetime.now, description="通知時間")
    message: str = Field(..., description="通知訊息")

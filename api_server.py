"""
FastAPI 伺服器
提供 REST API 和 WebSocket 端點
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse
from task_model import Task, TaskStatus
from task_service import task_service
from websocket_manager import manager
from typing import List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Task WebSocket API", version="1.0.0")


# HTML 測試客戶端
HTML_CLIENT = """
<!DOCTYPE html>
<html>
<head>
    <title>Task WebSocket 測試客戶端</title>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #333;
        }
        .container {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .status {
            padding: 10px;
            border-radius: 4px;
            margin-bottom: 10px;
        }
        .connected {
            background-color: #d4edda;
            color: #155724;
        }
        .disconnected {
            background-color: #f8d7da;
            color: #721c24;
        }
        #messages {
            height: 300px;
            overflow-y: auto;
            border: 1px solid #ddd;
            padding: 10px;
            background-color: #f9f9f9;
            border-radius: 4px;
        }
        .message {
            margin: 5px 0;
            padding: 8px;
            background-color: #e9ecef;
            border-radius: 4px;
            border-left: 4px solid #007bff;
        }
        button {
            background-color: #007bff;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            margin: 5px;
        }
        button:hover {
            background-color: #0056b3;
        }
        input, select {
            padding: 8px;
            margin: 5px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <h1>Task WebSocket 測試客戶端</h1>
    
    <div class="container">
        <div id="status" class="status disconnected">WebSocket 狀態: 未連接</div>
        <button onclick="connect()">連接 WebSocket</button>
        <button onclick="disconnect()">中斷連接</button>
    </div>

    <div class="container">
        <h2>建立新任務</h2>
        <input type="text" id="taskId" placeholder="任務 ID" />
        <input type="text" id="taskTitle" placeholder="任務標題" />
        <input type="text" id="taskDesc" placeholder="任務描述" />
        <select id="taskStatus">
            <option value="TO DO">TO DO</option>
            <option value="IN PROGRESS">IN PROGRESS</option>
            <option value="DONE">DONE</option>
        </select>
        <button onclick="createTask()">建立任務</button>
    </div>

    <div class="container">
        <h2>更新任務狀態</h2>
        <input type="text" id="updateTaskId" placeholder="任務 ID" />
        <select id="updateStatus">
            <option value="TO DO">TO DO</option>
            <option value="IN PROGRESS">IN PROGRESS</option>
            <option value="DONE">DONE</option>
        </select>
        <button onclick="updateTaskStatus()">更新狀態</button>
    </div>

    <div class="container">
        <h2>WebSocket 訊息</h2>
        <button onclick="clearMessages()">清除訊息</button>
        <div id="messages"></div>
    </div>

    <script>
        let ws = null;
        const messagesDiv = document.getElementById('messages');
        const statusDiv = document.getElementById('status');

        function connect() {
            if (ws) {
                addMessage('已經連接到 WebSocket');
                return;
            }

            ws = new WebSocket('ws://localhost:8000/ws');
            
            ws.onopen = function(event) {
                statusDiv.className = 'status connected';
                statusDiv.textContent = 'WebSocket 狀態: 已連接';
                addMessage('WebSocket 連接成功');
            };
            
            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                addMessage('收到通知: ' + JSON.stringify(data, null, 2));
            };
            
            ws.onerror = function(error) {
                addMessage('WebSocket 錯誤: ' + error.message);
            };
            
            ws.onclose = function(event) {
                statusDiv.className = 'status disconnected';
                statusDiv.textContent = 'WebSocket 狀態: 未連接';
                addMessage('WebSocket 連接已關閉');
                ws = null;
            };
        }

        function disconnect() {
            if (ws) {
                ws.close();
            }
        }

        async function createTask() {
            const taskId = document.getElementById('taskId').value;
            const taskTitle = document.getElementById('taskTitle').value;
            const taskDesc = document.getElementById('taskDesc').value;
            const taskStatus = document.getElementById('taskStatus').value;

            const response = await fetch('/tasks', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    id: taskId,
                    title: taskTitle,
                    description: taskDesc,
                    task_type: taskStatus
                })
            });

            const result = await response.json();
            addMessage('建立任務成功: ' + JSON.stringify(result, null, 2));
        }

        async function updateTaskStatus() {
            const taskId = document.getElementById('updateTaskId').value;
            const status = document.getElementById('updateStatus').value;

            const response = await fetch(`/tasks/${taskId}/status`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    status: status
                })
            });

            const result = await response.json();
            addMessage('更新任務狀態成功: ' + JSON.stringify(result, null, 2));
        }

        function addMessage(message) {
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message';
            messageDiv.textContent = new Date().toLocaleTimeString() + ' - ' + message;
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }

        function clearMessages() {
            messagesDiv.innerHTML = '';
        }
    </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def get_client():
    """取得測試客戶端頁面"""
    return HTML_CLIENT


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket 端點"""
    await manager.connect(websocket)
    try:
        while True:
            # 保持連接開啟，接收來自客戶端的訊息（如果有）
            data = await websocket.receive_text()
            logger.info(f"收到客戶端訊息: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("客戶端已中斷連接")


@app.post("/tasks", response_model=Task)
async def create_task(task: Task):
    """建立新任務"""
    return task_service.create_task(task)


@app.get("/tasks", response_model=List[Task])
async def get_all_tasks():
    """取得所有任務"""
    return task_service.get_all_tasks()


@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: str):
    """取得指定任務"""
    task = task_service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任務不存在")
    return task


@app.put("/tasks/{task_id}/status", response_model=Task)
async def update_task_status(task_id: str, status: dict):
    """
    更新任務狀態
    
    當任務狀態變更為 TO DO、IN PROGRESS 或 DONE 時，
    會自動透過 WebSocket 通知所有連接的客戶端
    """
    new_status = TaskStatus(status["status"])
    task = await task_service.update_task_status(task_id, new_status)
    if not task:
        raise HTTPException(status_code=404, detail="任務不存在")
    return task


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    """刪除任務"""
    if not task_service.delete_task(task_id):
        raise HTTPException(status_code=404, detail="任務不存在")
    return {"message": "任務已刪除"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

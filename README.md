# 計算機與任務管理系統

## 專案簡介

本專案包含兩個主要模組：

1. **計算機模組** - 提供基本的數學運算和微分功能
2. **任務管理模組** - 提供任務管理和 WebSocket 即時通知功能

## 功能特色

### 計算機功能
- 基本運算：加、減、乘、除
- 微分：數值估計一階導數（中央差分、五點中央差分）
- 運算歷史記錄

### 任務管理功能
- 任務的 CRUD 操作
- 任務狀態管理（TO DO、IN PROGRESS、DONE）
- **WebSocket 即時通知**：當任務狀態變更時，自動通知所有連接的客戶端
- RESTful API

## 技術架構

### 使用技術
- **程式語言**：Python 3.13+
- **Web 框架**：FastAPI
- **WebSocket**：原生 WebSocket 支援
- **測試框架**：pytest, pytest-asyncio
- **資料驗證**：Pydantic

### 設計原則
本專案遵循 **SOLID 原則**：

1. **單一職責原則 (SRP)**：每個類別只負責一項職責
   - `Calculator`：負責數學運算
   - `TaskService`：負責任務業務邏輯
   - `ConnectionManager`：負責 WebSocket 連接管理
   - `InMemoryTaskRepository`：負責任務資料存儲

2. **開放封閉原則 (OCP)**：對擴展開放，對修改封閉
   - 透過介面定義，易於擴展新的通知方式或儲存方式

3. **里氏替換原則 (LSP)**：子類別可以替換父類別
   - 所有介面實作都可以互相替換

4. **介面隔離原則 (ISP)**：不強迫客戶端依賴不使用的介面
   - `INotificationService` 和 `ITaskRepository` 分離

5. **依賴反轉原則 (DIP)**：依賴抽象而非具體實作
   - `TaskService` 依賴 `INotificationService` 和 `ITaskRepository` 介面

## 安裝與執行

### 安裝依賴
```bash
pip3 install -r requirements.txt
```

### 啟動 API 伺服器
```bash
python3 api_server.py
```

伺服器將在 `http://localhost:8000` 啟動。

### 使用測試客戶端
開啟瀏覽器訪問 `http://localhost:8000`，即可看到內建的 WebSocket 測試客戶端。

## API 文件

### REST API 端點

#### 任務管理
- `POST /tasks` - 建立新任務
- `GET /tasks` - 取得所有任務
- `GET /tasks/{task_id}` - 取得指定任務
- `PUT /tasks/{task_id}/status` - 更新任務狀態（會觸發 WebSocket 通知）
- `DELETE /tasks/{task_id}` - 刪除任務

#### WebSocket 端點
- `WS /ws` - WebSocket 連接端點，用於接收任務狀態變更通知

### API 使用範例

#### 建立任務
```bash
curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "task-1",
    "title": "完成專案文件",
    "description": "撰寫 README 和 API 文件",
    "task_type": "TO DO"
  }'
```

#### 更新任務狀態
```bash
curl -X PUT "http://localhost:8000/tasks/task-1/status" \
  -H "Content-Type: application/json" \
  -d '{"status": "IN PROGRESS"}'
```

當任務狀態更新時，所有連接的 WebSocket 客戶端將收到如下通知：
```json
{
  "type": "task_status_update",
  "data": {
    "task_id": "task-1",
    "title": "完成專案文件",
    "old_status": "TO DO",
    "new_status": "IN PROGRESS",
    "timestamp": "2025-10-13T12:00:00",
    "message": "任務「完成專案文件」狀態已從「TO DO」變更為「IN PROGRESS」"
  }
}
```

## WebSocket 通知機制

### 自動通知觸發條件
當任務狀態變更為以下三種狀態時，系統會自動透過 WebSocket 通知所有連接的客戶端：

1. **TO DO** - 任務被設定為待辦
2. **IN PROGRESS** - 任務開始進行
3. **DONE** - 任務完成

### 通知流程
1. 客戶端透過 WebSocket 連接到 `/ws` 端點
2. 客戶端或其他系統呼叫 `PUT /tasks/{task_id}/status` API 更新任務狀態
3. `TaskService` 更新任務狀態並建立通知訊息
4. `WebSocketNotificationService` 透過 `ConnectionManager` 廣播通知
5. 所有連接的客戶端即時收到狀態變更通知

## 計算機功能使用說明

### 啟動計算機
```bash
python3 main.py
```

### 微分功能
在主選單選擇「7. 微分」，根據提示：
- 輸入函數表達式（變數為 `x`），可使用 `math` 模組中的函數，例如 `sin(x)`, `cos(x)`, `exp(x)`, `log(x)` 等。
- 輸入評估點 `x`。
- 可選擇數值方法：
  - 五點中央差分（預設，精度 O(h^4)）
  - 中央差分（精度 O(h^2)）
- 可設定步長 `h`（預設 1e-5）。

### 範例
- `f(x) = x**2 + 3*x + 1`，在 `x = 2` 的導數近似為 `2*x + 3 = 7`。
- `f(x) = sin(x)`，在 `x = 0.7` 的導數近似為 `cos(0.7)`。

## 測試

### 執行單元測試
```bash
# 執行所有測試
python3 -m pytest -v

# 執行 WebSocket 通知測試
python3 -m pytest test_websocket_notification.py -v

# 執行計算機測試
python3 -m pytest test_calculator.py -v
```

### 測試覆蓋範圍
- ✅ 任務建立、查詢、更新、刪除
- ✅ WebSocket 通知功能（TO DO、IN PROGRESS、DONE 狀態變更）
- ✅ 通知訊息格式驗證
- ✅ 多次狀態更新測試
- ✅ 錯誤處理（不存在的任務）
- ✅ 計算機基本運算
- ✅ 數值微分功能

## 專案結構

```
.
├── README.md                          # 專案說明文件
├── 類別圖.md                          # Mermaid 類別圖文件
├── requirements.txt                    # Python 依賴套件
│
├── main.py                            # 計算機主程式
├── calculator.py                      # 計算機模組
├── test_calculator.py                 # 計算機測試
│
├── task_model.py                      # 任務資料模型
├── notification_interface.py          # 通知服務介面（SOLID - DIP）
├── task_service.py                    # 任務服務（業務邏輯）
├── websocket_manager.py               # WebSocket 連接管理器
├── api_server.py                      # FastAPI 應用程式
└── test_websocket_notification.py     # WebSocket 通知測試
```

## 類別圖

詳細的類別關係圖請參考 [類別圖.md](./類別圖.md)。

## 未來改進方向

1. **資料持久化**：目前使用記憶體儲存，可改用資料庫（PostgreSQL、MongoDB）
2. **身份驗證**：加入 JWT 或 OAuth2 身份驗證
3. **任務優先級**：新增任務優先級和截止日期功能
4. **通知過濾**：允許客戶端訂閱特定任務或狀態的通知
5. **效能優化**：加入快取機制和連接池管理
6. **Docker 容器化**：建立 Dockerfile 和 docker-compose.yml

## 授權

本專案採用 MIT 授權條款。

## 作者

計算機與任務管理系統開發團隊

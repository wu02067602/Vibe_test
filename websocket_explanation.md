# WebSocket 說明文件

## 目錄
- [什麼是 WebSocket？](#什麼是-websocket)
- [WebSocket 的特性](#websocket-的特性)
- [WebSocket vs HTTP](#websocket-vs-http)
- [WebSocket 工作原理](#websocket-工作原理)
- [使用場景](#使用場景)
- [Python 實作範例](#python-實作範例)
- [最佳實踐](#最佳實踐)

## 什麼是 WebSocket？

WebSocket 是一種在單一 TCP 連線上進行全雙工通訊的協定。它允許伺服器與客戶端之間建立持久性的連線，雙方可以在任何時候主動發送資料，而不需要等待對方的請求。

WebSocket 協定在 2011 年由 IETF 標準化為 RFC 6455，並由 HTML5 規範引入到 Web 瀏覽器中。

## WebSocket 的特性

### 1. **全雙工通訊**
- 客戶端和伺服器可以同時發送和接收資料
- 不需要等待請求-回應週期

### 2. **持久連線**
- 建立連線後保持開啟狀態
- 減少建立和關閉連線的開銷

### 3. **低延遲**
- 資料可以即時傳輸
- 沒有 HTTP 請求的額外開銷

### 4. **輕量級協定**
- 資料幀的標頭很小（2-14 bytes）
- 相比 HTTP 請求標頭（數百 bytes）更有效率

### 5. **支援文字和二進位資料**
- 可以傳輸文字訊息（UTF-8）
- 可以傳輸二進位資料（如圖片、檔案）

## WebSocket vs HTTP

| 特性 | HTTP | WebSocket |
|------|------|-----------|
| **通訊模式** | 請求-回應（半雙工） | 全雙工 |
| **連線狀態** | 無狀態，每次請求建立新連線 | 有狀態，持久連線 |
| **伺服器推送** | 不支援（需使用輪詢） | 原生支援 |
| **標頭大小** | 較大（數百 bytes） | 較小（2-14 bytes） |
| **延遲** | 較高 | 較低 |
| **適用場景** | 一般的 Web 請求 | 即時通訊應用 |

## WebSocket 工作原理

### 1. **握手階段（Handshake）**

WebSocket 連線始於 HTTP 升級請求：

```http
GET /chat HTTP/1.1
Host: example.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13
```

伺服器回應：

```http
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
```

### 2. **資料傳輸**

握手成功後，連線升級為 WebSocket 協定，雙方可以開始傳輸資料幀。

### 3. **關閉連線**

任一方都可以發送關閉幀來終止連線。

## 使用場景

### 1. **即時聊天應用**
- 訊息即時傳遞
- 線上狀態更新
- 打字指示器

### 2. **線上遊戲**
- 多人遊戲同步
- 即時遊戲狀態更新

### 3. **即時協作工具**
- 線上文件編輯（如 Google Docs）
- 白板應用
- 程式碼協作編輯

### 4. **金融交易平台**
- 股票價格即時更新
- 交易通知

### 5. **監控儀表板**
- 系統狀態監控
- 日誌即時顯示
- IoT 裝置資料推送

### 6. **通知系統**
- 推播通知
- 警報系統

## Python 實作範例

### 使用 websockets 函式庫（伺服器端）

```python
import asyncio
import websockets

async def echo_handler(websocket, path):
    """處理 WebSocket 連線的處理器"""
    print(f"新客戶端連線: {websocket.remote_address}")
    
    try:
        async for message in websocket:
            print(f"收到訊息: {message}")
            # 回傳訊息給客戶端
            await websocket.send(f"伺服器收到: {message}")
    except websockets.exceptions.ConnectionClosed:
        print("客戶端斷線")

async def main():
    # 啟動 WebSocket 伺服器
    server = await websockets.serve(echo_handler, "localhost", 8765)
    print("WebSocket 伺服器啟動於 ws://localhost:8765")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
```

### 使用 websockets 函式庫（客戶端）

```python
import asyncio
import websockets

async def client():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        # 發送訊息
        await websocket.send("你好，伺服器！")
        print("已發送: 你好，伺服器！")
        
        # 接收回應
        response = await websocket.recv()
        print(f"收到回應: {response}")

if __name__ == "__main__":
    asyncio.run(client())
```

### 使用 Flask-SocketIO（整合 Flask）

```python
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(data):
    print(f'收到訊息: {data}')
    emit('response', {'data': f'伺服器收到: {data}'})

@socketio.on('connect')
def handle_connect():
    print('客戶端已連線')
    emit('response', {'data': '已連線到伺服器'})

@socketio.on('disconnect')
def handle_disconnect():
    print('客戶端已斷線')

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)
```

### JavaScript 客戶端範例

```javascript
// 建立 WebSocket 連線
const socket = new WebSocket('ws://localhost:8765');

// 連線開啟時
socket.addEventListener('open', (event) => {
    console.log('已連線到 WebSocket 伺服器');
    socket.send('你好，伺服器！');
});

// 接收訊息時
socket.addEventListener('message', (event) => {
    console.log('收到訊息:', event.data);
});

// 發生錯誤時
socket.addEventListener('error', (event) => {
    console.error('WebSocket 錯誤:', event);
});

// 連線關閉時
socket.addEventListener('close', (event) => {
    console.log('WebSocket 連線已關閉');
});
```

## 最佳實踐

### 1. **錯誤處理**
```python
try:
    async for message in websocket:
        # 處理訊息
        pass
except websockets.exceptions.ConnectionClosed:
    # 處理連線關閉
    pass
except Exception as e:
    # 處理其他錯誤
    print(f"錯誤: {e}")
```

### 2. **心跳機制（Ping/Pong）**
```python
async def heartbeat(websocket):
    while True:
        try:
            await websocket.ping()
            await asyncio.sleep(30)  # 每 30 秒發送一次 ping
        except:
            break
```

### 3. **訊息驗證**
```python
import json

async def handle_message(websocket, message):
    try:
        data = json.loads(message)
        # 驗證訊息格式
        if 'type' not in data or 'payload' not in data:
            await websocket.send(json.dumps({
                'error': '無效的訊息格式'
            }))
            return
        # 處理訊息
    except json.JSONDecodeError:
        await websocket.send(json.dumps({
            'error': '無效的 JSON'
        }))
```

### 4. **連線管理**
```python
# 管理所有活躍連線
active_connections = set()

async def handler(websocket, path):
    # 註冊連線
    active_connections.add(websocket)
    try:
        async for message in websocket:
            # 廣播訊息給所有客戶端
            await asyncio.gather(
                *[ws.send(message) for ws in active_connections]
            )
    finally:
        # 移除連線
        active_connections.remove(websocket)
```

### 5. **安全性考量**

- **使用 WSS（WebSocket Secure）**：在生產環境中使用加密連線
- **驗證來源**：檢查 Origin 標頭防止 CSRF 攻擊
- **身份驗證**：實作適當的身份驗證機制
- **訊息大小限制**：限制訊息大小防止 DoS 攻擊
- **速率限制**：限制客戶端發送訊息的頻率

```python
# 使用 WSS
import ssl

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain('cert.pem', 'key.pem')

server = await websockets.serve(
    handler, 
    "localhost", 
    8765,
    ssl=ssl_context
)
```

### 6. **資源清理**
```python
async def handler(websocket, path):
    try:
        # 處理連線
        pass
    finally:
        # 確保資源被正確釋放
        await websocket.close()
```

## 常見問題

### Q1: WebSocket 和 Socket.IO 有什麼區別？
**A:** WebSocket 是一個協定，而 Socket.IO 是一個函式庫，它在 WebSocket 的基礎上提供了額外的功能（如自動重連、房間支援等），並在不支援 WebSocket 時自動降級到其他傳輸方式（如長輪詢）。

### Q2: WebSocket 連線會自動重連嗎？
**A:** 原生 WebSocket API 不會自動重連，需要自己實作重連邏輯。但許多函式庫（如 Socket.IO）提供了自動重連功能。

### Q3: WebSocket 支援跨域嗎？
**A:** 是的，但伺服器需要正確處理 CORS（跨域資源共享）。可以透過檢查 Origin 標頭來控制哪些域可以連線。

### Q4: WebSocket 適合傳輸大量資料嗎？
**A:** WebSocket 適合傳輸頻繁但較小的訊息。對於大型檔案傳輸，可能還是使用 HTTP 更合適，可以利用分塊傳輸和斷點續傳等功能。

## 相關資源

- [RFC 6455 - WebSocket 協定規範](https://tools.ietf.org/html/rfc6455)
- [MDN WebSocket 文件](https://developer.mozilla.org/zh-TW/docs/Web/API/WebSocket)
- [websockets Python 函式庫](https://websockets.readthedocs.io/)
- [Flask-SocketIO 文件](https://flask-socketio.readthedocs.io/)

---

**建立日期**: 2025-10-12

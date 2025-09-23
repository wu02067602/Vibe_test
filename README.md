# 計算機專案 (Calculator Project)

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-stable-brightgreen.svg)

一個功能完整的命令列計算機應用程式，支援基本四則運算、數值微分和數值積分計算。

## 📋 目錄

- [功能特色](#功能特色)
- [系統需求](#系統需求)
- [安裝說明](#安裝說明)
- [使用方法](#使用方法)
- [功能詳解](#功能詳解)
- [API 文檔](#api-文檔)
- [測試](#測試)
- [專案結構](#專案結構)
- [技術說明](#技術說明)
- [範例](#範例)
- [故障排除](#故障排除)
- [貢獻指南](#貢獻指南)
- [版本歷史](#版本歷史)
- [授權](#授權)

## 🚀 功能特色

### 基本運算
- ✅ **四則運算**：加法、減法、乘法、除法
- ✅ **浮點數支援**：完整的小數運算
- ✅ **錯誤處理**：除零檢查和輸入驗證

### 進階數學功能
- ✅ **數值微分**：
  - 中央差分法（精度 O(h²)）
  - 五點中央差分法（精度 O(h⁴)）
  - 可調整步長和方法
  
- ✅ **數值積分**：
  - Simpson 法則（1/3 法則，高精度）
  - 梯形法則（快速計算）
  - 可調整分割數量

### 系統功能
- ✅ **運算歷史**：自動記錄所有計算過程
- ✅ **表達式解析**：支援數學函數（sin, cos, exp, log 等）
- ✅ **安全評估**：限制執行環境，防止危險操作
- ✅ **友善介面**：直觀的命令列選單

## 💻 系統需求

- **Python 3.8 或更新版本**
- **作業系統**：Windows、macOS、Linux
- **記憶體**：最少 64MB RAM
- **磁碟空間**：約 1MB

### Python 套件相依性
```
無外部相依套件 - 僅使用 Python 標準庫：
- math: 數學函數
- sys: 系統功能
- typing: 類型提示
- unittest: 測試框架
```

## 📦 安裝說明

### 方法 1：直接下載
```bash
# 下載專案檔案
git clone <repository-url>
cd calculator-project

# 直接執行
python main.py
```

### 方法 2：檢查安裝
```bash
# 檢查 Python 版本
python --version

# 執行測試確認功能正常
python test_calculator.py

# 啟動計算機
python main.py
```

### Windows 使用者
```batch
# 使用批次檔執行
run.bat
```

### Unix/Linux/macOS 使用者
```bash
# 使用腳本執行
chmod +x run.sh
./run.sh
```

## 🎯 使用方法

### 啟動程式
```bash
python main.py
```

### 基本操作流程
1. 程式啟動後會顯示主選單
2. 輸入數字選擇功能（0-8）
3. 根據提示輸入相關參數
4. 查看計算結果
5. 按 Enter 繼續或選擇 0 退出

### 快速開始範例
```
========================================
           計算機
========================================
1. 加法 (+)
2. 減法 (-)
3. 乘法 (×)
4. 除法 (÷)
7. 微分 d/dx [輸入函數表達式]
8. 積分 ∫ [輸入函數表達式]
5. 查看運算歷史
6. 清除歷史
0. 離開
========================================
請選擇功能 (0-8): 1
```

## 📖 功能詳解

### 1. 基本四則運算（選項 1-4）
支援標準的數學運算，包含完整的錯誤處理。

**特色：**
- 支援正負數和小數
- 自動除零檢查
- 結果自動記錄到歷史

**使用範例：**
```
選擇: 1 (加法)
第一個數字: 3.5
第二個數字: 2.1
結果: 5.6
```

### 2. 數值微分（選項 7）
計算函數在指定點的導數近似值。

**支援方法：**
- **五點中央差分**（預設）：`f'(x) ≈ [f(x-2h) - 8f(x-h) + 8f(x+h) - f(x+2h)] / (12h)`
- **中央差分**：`f'(x) ≈ [f(x+h) - f(x-h)] / (2h)`

**可調整參數：**
- 評估點 x
- 步長 h（預設 1e-5）
- 數值方法

**使用範例：**
```
f(x) = x**2 + 3*x + 1
評估點 x: 2
方法: 五點中央差分
步長: 1e-5
結果: f'(2) ≈ 7.000000 （理論值：2×2 + 3 = 7）
```

### 3. 數值積分（選項 8）
計算函數在指定區間的定積分近似值。

**支援方法：**
- **Simpson 法則**（預設）：使用拋物線近似，精度較高
- **梯形法則**：使用梯形近似，計算較快

**可調整參數：**
- 積分下限 a
- 積分上限 b
- 分割數量 n（預設 1000）
- 數值方法

**使用範例：**
```
f(x) = x**2
下限 a: 0
上限 b: 3
方法: Simpson 法則
分割數: 1000
結果: ∫₀³ x² dx ≈ 9.000000 （理論值：x³/3|₀³ = 9）
```

### 4. 運算歷史管理（選項 5-6）
- **查看歷史**（選項 5）：顯示所有運算記錄
- **清除歷史**（選項 6）：清空所有記錄

### 5. 支援的數學函數
程式支援 Python math 模組中的所有函數：

**三角函數：**
- `sin(x)`, `cos(x)`, `tan(x)`
- `asin(x)`, `acos(x)`, `atan(x)`, `atan2(y,x)`
- `sinh(x)`, `cosh(x)`, `tanh(x)`

**指數和對數：**
- `exp(x)`, `log(x)`, `log10(x)`, `log2(x)`
- `pow(x,y)`, `sqrt(x)`

**其他函數：**
- `ceil(x)`, `floor(x)`, `fabs(x)`
- `factorial(x)`, `gcd(a,b)`

**常數：**
- `pi` (π ≈ 3.14159...)
- `e` (自然常數 ≈ 2.71828...)

## 📚 API 文檔

### Calculator 類別

#### 初始化
```python
from calculator import Calculator
calc = Calculator()
```

#### 基本運算方法
```python
# 加法
result = calc.add(a: float, b: float) -> float

# 減法  
result = calc.subtract(a: float, b: float) -> float

# 乘法
result = calc.multiply(a: float, b: float) -> float

# 除法（會檢查除零）
result = calc.divide(a: float, b: float) -> float

# 統一運算介面
result = calc.calculate(operation: str, a: float, b: float) -> float
```

#### 進階數學方法
```python
# 數值微分
result = calc.derivative(
    func: Callable[[float], float],  # 函數
    x: float,                        # 評估點
    h: float = 1e-5,                # 步長
    method: str = 'five_point',     # 方法
    label: Optional[str] = None     # 標籤
) -> float

# 數值積分
result = calc.integrate(
    func: Callable[[float], float],  # 函數
    a: float,                        # 下限
    b: float,                        # 上限
    n: int = 1000,                  # 分割數
    method: str = 'simpson',        # 方法
    label: Optional[str] = None     # 標籤
) -> float
```

#### 歷史管理方法
```python
# 取得歷史
history = calc.get_history() -> list[str]

# 清除歷史
calc.clear_history() -> None
```

### 輔助函數

#### 表達式解析
```python
from main import build_function_from_expr

# 建立函數
f = build_function_from_expr("x**2 + sin(x)")
result = f(1.5)  # 計算 1.5² + sin(1.5)
```

## 🧪 測試

### 執行完整測試套件
```bash
python test_calculator.py
```

### 測試涵蓋範圍
- ✅ 基本四則運算
- ✅ 錯誤處理（除零、無效輸入）
- ✅ 數值微分（多種方法和函數）
- ✅ 數值積分（多種方法和函數）
- ✅ 歷史記錄功能
- ✅ 邊界條件測試

### 測試結果範例
```
執行計算機測試...
test_addition (__main__.TestCalculator.test_addition)
測試加法 ... ok
test_integrate_simpson (__main__.TestCalculator.test_integrate_simpson)
測試 Simpson 法則積分 ... ok
...
----------------------------------------------------------------------
Ran 16 tests in 0.006s

OK
```

## 📁 專案結構

```
calculator-project/
│
├── main.py              # 主程式檔案
├── calculator.py        # 計算機核心類別
├── test_calculator.py   # 測試檔案
├── README.md           # 專案文檔（本檔案）
├── requirements.txt    # Python 套件需求
├── run.bat            # Windows 執行腳本
├── run.sh             # Unix/Linux 執行腳本
└── git_error_docs.md  # Git 相關文檔
```

### 檔案說明

| 檔案 | 描述 | 重要性 |
|------|------|--------|
| `main.py` | 主程式，提供命令列介面 | ⭐⭐⭐ |
| `calculator.py` | 核心計算邏輯和數學函數 | ⭐⭐⭐ |
| `test_calculator.py` | 完整的測試套件 | ⭐⭐ |
| `README.md` | 專案文檔和使用說明 | ⭐⭐ |
| `requirements.txt` | 相依套件列表 | ⭐ |

## 🔧 技術說明

### 數值方法理論

#### 數值微分
**中央差分法：**
```
f'(x) ≈ [f(x+h) - f(x-h)] / (2h)
誤差階數：O(h²)
```

**五點中央差分法：**
```
f'(x) ≈ [f(x-2h) - 8f(x-h) + 8f(x+h) - f(x+2h)] / (12h)
誤差階數：O(h⁴)
```

#### 數值積分
**梯形法則：**
```
∫[a,b] f(x)dx ≈ (h/2)[f(a) + 2∑f(xi) + f(b)]
其中 h = (b-a)/n，xi = a + ih
```

**Simpson 法則：**
```
∫[a,b] f(x)dx ≈ (h/3)[f(a) + 4∑f(x_odd) + 2∑f(x_even) + f(b)]
需要偶數個分割
```

### 安全性設計
- **限制執行環境**：禁用 `__builtins__`，防止執行危險函數
- **白名單機制**：只允許 math 模組中的函數
- **輸入驗證**：完整的參數檢查和錯誤處理
- **異常捕捉**：多層次的錯誤處理機制

## 📝 範例

### 範例 1：基本運算
```python
from calculator import Calculator

calc = Calculator()
result = calc.add(10.5, 3.2)
print(f"10.5 + 3.2 = {result}")  # 13.7
```

### 範例 2：微分計算
```python
import math
from calculator import Calculator

calc = Calculator()

# 定義函數 f(x) = x²
f = lambda x: x**2

# 計算 f'(2)，理論值為 4
derivative = calc.derivative(f, 2.0)
print(f"f'(2) = {derivative:.6f}")  # 約 4.000000
```

### 範例 3：積分計算
```python
import math
from calculator import Calculator

calc = Calculator()

# 計算 sin(x) 從 0 到 π 的積分，理論值為 2
integral = calc.integrate(math.sin, 0, math.pi)
print(f"∫₀^π sin(x)dx = {integral:.6f}")  # 約 2.000000
```

### 範例 4：複雜函數
```python
from main import build_function_from_expr
from calculator import Calculator

calc = Calculator()

# 建立複雜函數
f = build_function_from_expr("exp(x) * sin(x) + log(x)")

# 計算積分
result = calc.integrate(f, 1, 2, n=5000)
print(f"積分結果: {result}")
```

## 🔍 故障排除

### 常見問題

#### Q1: 程式無法啟動
**症狀：** 執行 `python main.py` 時出現錯誤
**解決方案：**
```bash
# 檢查 Python 版本
python --version

# 確保版本 >= 3.8
# 如果版本過舊，請升級 Python
```

#### Q2: 函數表達式解析失敗
**症狀：** 輸入函數表達式後出現 "無法解析" 錯誤
**解決方案：**
- 確保使用 `x` 作為變數名稱
- 使用正確的 Python 語法（如 `x**2` 而不是 `x^2`）
- 檢查函數名稱是否正確（如 `sin(x)` 而不是 `Sin(x)`）

#### Q3: 數值結果不準確
**症狀：** 微分或積分結果與理論值相差較大
**解決方案：**
- 微分：減小步長 h（如 1e-8）
- 積分：增加分割數量 n（如 10000）
- 選擇更高精度的方法（五點中央差分、Simpson 法則）

#### Q4: 記憶體使用過多
**症狀：** 程式運行緩慢或記憶體不足
**解決方案：**
- 減少積分的分割數量
- 清除運算歷史
- 避免計算極大區間的積分

### 錯誤碼對照

| 錯誤訊息 | 原因 | 解決方法 |
|----------|------|----------|
| "除數不能為零" | 嘗試除以零 | 確保除數不為零 |
| "積分上限必須大於下限" | a >= b | 確保 b > a |
| "步長 h 必須為正數" | h <= 0 | 使用正數步長 |
| "函數評估失敗" | 函數計算錯誤 | 檢查函數定義域 |

## 🤝 貢獻指南

歡迎貢獻！請遵循以下步驟：

### 1. 環境設置
```bash
git clone <repository-url>
cd calculator-project
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. 開發規範
- 遵循 PEP 8 編碼風格
- 添加適當的類型提示
- 撰寫詳細的文檔字串
- 為新功能添加測試

### 3. 測試要求
```bash
# 執行所有測試
python test_calculator.py

# 確保所有測試通過
```

### 4. 提交規範
- 使用清楚的提交訊息
- 一次提交一個功能
- 更新相關文檔

## 📋 版本歷史

### v1.1.0 (最新)
- ✅ 添加數值積分功能
- ✅ 支援 Simpson 法則和梯形法則
- ✅ 完善的文檔和註解
- ✅ 擴展測試套件

### v1.0.0
- ✅ 基本四則運算
- ✅ 數值微分功能
- ✅ 運算歷史記錄
- ✅ 命令列介面

### 未來計劃 (v1.2.0)
- 🔄 圖形使用者介面 (GUI)
- 🔄 更多數值方法
- 🔄 函數繪圖功能
- 🔄 結果匯出功能

## 📄 授權

本專案採用 MIT 授權條款。詳見 [LICENSE](LICENSE) 檔案。

```
MIT License

Copyright (c) 2024 Calculator Project

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

## 📞 聯絡資訊

- **專案維護者**：AI Assistant
- **問題回報**：請使用 GitHub Issues
- **功能建議**：歡迎提交 Pull Request

---

**感謝使用計算機專案！** 🎉

如果這個專案對您有幫助，請給我們一個 ⭐ Star！
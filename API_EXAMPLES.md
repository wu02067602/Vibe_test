# API 文檔和使用範例

## 概述

本文檔提供計算機專案的完整 API 使用指南和實用範例，幫助開發者快速上手和集成計算機功能。

## 目錄

1. [快速開始](#快速開始)
2. [Calculator 類別 API](#calculator-類別-api)
3. [基本運算範例](#基本運算範例)
4. [數值微分範例](#數值微分範例)
5. [數值積分範例](#數值積分範例)
6. [進階使用案例](#進階使用案例)
7. [錯誤處理](#錯誤處理)
8. [性能優化建議](#性能優化建議)

## 快速開始

### 安裝和匯入

```python
# 確保檔案在同一目錄或 Python 路徑中
from calculator import Calculator
import math
```

### 基本使用

```python
# 建立計算機實例
calc = Calculator()

# 執行基本運算
result = calc.add(10, 5)
print(f"10 + 5 = {result}")  # 輸出: 10 + 5 = 15

# 查看運算歷史
history = calc.get_history()
print(history)  # ['10 + 5 = 15']
```

## Calculator 類別 API

### 建構函數

```python
Calculator()
```

建立新的計算機實例，初始化空的運算歷史。

**範例：**
```python
calc = Calculator()
```

---

### 基本運算方法

#### add(a, b)

執行加法運算。

**參數：**
- `a` (float): 第一個加數
- `b` (float): 第二個加數

**回傳：**
- `float`: 兩數相加的結果

**範例：**
```python
result = calc.add(3.5, 2.1)
print(result)  # 5.6
```

#### subtract(a, b)

執行減法運算。

**參數：**
- `a` (float): 被減數
- `b` (float): 減數

**回傳：**
- `float`: 兩數相減的結果

**範例：**
```python
result = calc.subtract(10, 3)
print(result)  # 7
```

#### multiply(a, b)

執行乘法運算。

**參數：**
- `a` (float): 第一個乘數
- `b` (float): 第二個乘數

**回傳：**
- `float`: 兩數相乘的結果

**範例：**
```python
result = calc.multiply(4, 2.5)
print(result)  # 10.0
```

#### divide(a, b)

執行除法運算。

**參數：**
- `a` (float): 被除數
- `b` (float): 除數

**回傳：**
- `float`: 兩數相除的結果

**拋出：**
- `ValueError`: 當除數為零時

**範例：**
```python
result = calc.divide(15, 3)
print(result)  # 5.0

# 除零錯誤
try:
    calc.divide(10, 0)
except ValueError as e:
    print(f"錯誤: {e}")  # 錯誤: 除數不能為零
```

#### calculate(operation, a, b)

統一的運算介面。

**參數：**
- `operation` (str): 運算符號 ('+', '-', '*', '/')
- `a` (float): 第一個運算數
- `b` (float): 第二個運算數

**回傳：**
- `float`: 運算結果

**拋出：**
- `ValueError`: 當運算符號不支援時

**範例：**
```python
result = calc.calculate('+', 10, 5)
print(result)  # 15.0

result = calc.calculate('*', 3, 4)
print(result)  # 12.0
```

---

### 數值微分方法

#### derivative(func, x, h=1e-5, method='five_point', label=None)

計算函數在指定點的數值微分。

**參數：**
- `func` (callable): 要微分的函數
- `x` (float): 計算導數的點
- `h` (float, optional): 步長，預設 1e-5
- `method` (str, optional): 數值方法，'central' 或 'five_point'，預設 'five_point'
- `label` (str, optional): 函數標籤，用於歷史記錄

**回傳：**
- `float`: 導數近似值

**支援的方法：**
- `'central'`: 中央差分法，精度 O(h²)
- `'five_point'`: 五點中央差分法，精度 O(h⁴)

**範例：**
```python
import math

# 定義函數
f = lambda x: x**2 + 3*x + 1

# 計算導數
derivative = calc.derivative(f, 2.0, method='five_point')
print(f"f'(2) = {derivative}")  # f'(2) = 7.0 (理論值: 2*2 + 3 = 7)

# 使用 math 函數
sin_derivative = calc.derivative(math.sin, math.pi/4)
print(f"sin'(π/4) = {sin_derivative:.6f}")  # 約 0.707107 (cos(π/4))
```

---

### 數值積分方法

#### integrate(func, a, b, n=1000, method='simpson', label=None)

計算函數在指定區間的數值積分。

**參數：**
- `func` (callable): 要積分的函數
- `a` (float): 積分下限
- `b` (float): 積分上限
- `n` (int, optional): 分割數量，預設 1000
- `method` (str, optional): 數值方法，'simpson' 或 'trapezoidal'，預設 'simpson'
- `label` (str, optional): 函數標籤，用於歷史記錄

**回傳：**
- `float`: 積分近似值

**支援的方法：**
- `'simpson'`: Simpson 法則，精度較高
- `'trapezoidal'`: 梯形法則，計算較快

**範例：**
```python
import math

# 定義函數
f = lambda x: x**2

# 計算積分
integral = calc.integrate(f, 0, 3, method='simpson')
print(f"∫₀³ x² dx = {integral}")  # 9.0 (理論值: x³/3|₀³ = 9)

# 使用 math 函數
sin_integral = calc.integrate(math.sin, 0, math.pi)
print(f"∫₀^π sin(x) dx = {sin_integral:.6f}")  # 約 2.0
```

---

### 歷史管理方法

#### get_history()

取得所有運算歷史記錄。

**回傳：**
- `list[str]`: 包含所有運算記錄的列表

**範例：**
```python
calc.add(2, 3)
calc.multiply(4, 5)
history = calc.get_history()
print(history)
# ['2 + 3 = 5', '4 × 5 = 20']
```

#### clear_history()

清除所有運算歷史記錄。

**範例：**
```python
calc.add(1, 2)
print(len(calc.get_history()))  # 1

calc.clear_history()
print(len(calc.get_history()))  # 0
```

---

## 基本運算範例

### 範例 1: 簡單計算

```python
from calculator import Calculator

calc = Calculator()

# 執行各種運算
print("=== 基本運算範例 ===")
print(f"加法: 12.5 + 7.3 = {calc.add(12.5, 7.3)}")
print(f"減法: 20 - 8 = {calc.subtract(20, 8)}")
print(f"乘法: 6 × 7 = {calc.multiply(6, 7)}")
print(f"除法: 45 ÷ 9 = {calc.divide(45, 9)}")

# 查看歷史
print("\n運算歷史:")
for i, record in enumerate(calc.get_history(), 1):
    print(f"{i}. {record}")
```

### 範例 2: 連續運算

```python
from calculator import Calculator

calc = Calculator()

# 連續運算範例：計算 (10 + 5) × 3 - 8
step1 = calc.add(10, 5)        # 15
step2 = calc.multiply(step1, 3) # 45
step3 = calc.subtract(step2, 8) # 37

print(f"最終結果: {step3}")
print("\n計算過程:")
for record in calc.get_history():
    print(record)
```

## 數值微分範例

### 範例 3: 多項式微分

```python
from calculator import Calculator

calc = Calculator()

# 定義多項式 f(x) = 2x³ - 3x² + 4x - 1
def polynomial(x):
    return 2*x**3 - 3*x**2 + 4*x - 1

# 計算在不同點的導數
points = [0, 1, 2, -1]
print("=== 多項式微分範例 ===")
print("f(x) = 2x³ - 3x² + 4x - 1")
print("f'(x) = 6x² - 6x + 4 (理論導數)")

for x in points:
    numerical = calc.derivative(polynomial, x, label=f"2x³-3x²+4x-1")
    theoretical = 6*x**2 - 6*x + 4
    print(f"x={x}: 數值={numerical:.6f}, 理論={theoretical}, 誤差={abs(numerical-theoretical):.2e}")
```

### 範例 4: 三角函數微分

```python
import math
from calculator import Calculator

calc = Calculator()

print("=== 三角函數微分範例 ===")

# sin(x) 的導數是 cos(x)
test_points = [0, math.pi/6, math.pi/4, math.pi/3, math.pi/2]

for x in test_points:
    numerical = calc.derivative(math.sin, x, method='five_point')
    theoretical = math.cos(x)
    print(f"sin'({x:.3f}) = {numerical:.6f} (理論: {theoretical:.6f})")
```

### 範例 5: 比較不同微分方法

```python
import math
from calculator import Calculator

calc = Calculator()

# 比較中央差分和五點中央差分的精度
f = lambda x: math.exp(x) * math.sin(x)  # e^x * sin(x)
x = 1.0

print("=== 微分方法比較 ===")
print(f"函數: f(x) = e^x * sin(x), 在 x = {x}")

# 理論導數: d/dx[e^x * sin(x)] = e^x * (sin(x) + cos(x))
theoretical = math.exp(x) * (math.sin(x) + math.cos(x))

# 數值方法
central = calc.derivative(f, x, method='central', h=1e-5)
five_point = calc.derivative(f, x, method='five_point', h=1e-5)

print(f"理論值: {theoretical:.8f}")
print(f"中央差分: {central:.8f} (誤差: {abs(central-theoretical):.2e})")
print(f"五點中央: {five_point:.8f} (誤差: {abs(five_point-theoretical):.2e})")
```

## 數值積分範例

### 範例 6: 基本積分計算

```python
import math
from calculator import Calculator

calc = Calculator()

print("=== 基本積分範例 ===")

# 範例 1: ∫₀² x² dx = x³/3|₀² = 8/3
f1 = lambda x: x**2
result1 = calc.integrate(f1, 0, 2)
theoretical1 = 8/3
print(f"∫₀² x² dx = {result1:.6f} (理論: {theoretical1:.6f})")

# 範例 2: ∫₀^π sin(x) dx = -cos(x)|₀^π = 2
result2 = calc.integrate(math.sin, 0, math.pi)
print(f"∫₀^π sin(x) dx = {result2:.6f} (理論: 2.000000)")

# 範例 3: ∫₁⁴ (1/x) dx = ln(x)|₁⁴ = ln(4)
f3 = lambda x: 1/x
result3 = calc.integrate(f3, 1, 4)
theoretical3 = math.log(4)
print(f"∫₁⁴ (1/x) dx = {result3:.6f} (理論: {theoretical3:.6f})")
```

### 範例 7: 比較積分方法

```python
import math
from calculator import Calculator

calc = Calculator()

# 比較 Simpson 法則和梯形法則
f = lambda x: math.exp(-x**2)  # 高斯函數
a, b = 0, 2

print("=== 積分方法比較 ===")
print(f"函數: f(x) = e^(-x²), 區間: [0, 2]")

# 使用不同方法和分割數
methods = ['simpson', 'trapezoidal']
n_values = [100, 1000, 10000]

for method in methods:
    print(f"\n{method.capitalize()} 法則:")
    for n in n_values:
        result = calc.integrate(f, a, b, n=n, method=method)
        print(f"  n={n:5d}: {result:.8f}")
```

### 範例 8: 複雜函數積分

```python
import math
from calculator import Calculator

calc = Calculator()

print("=== 複雜函數積分範例 ===")

# 定義複雜函數
functions = [
    (lambda x: x * math.sin(x), "x·sin(x)", 0, math.pi),
    (lambda x: math.exp(x) * math.cos(x), "e^x·cos(x)", 0, 1),
    (lambda x: 1 / (1 + x**2), "1/(1+x²)", 0, 1),  # 這個積分等於 π/4
]

for func, name, a, b in functions:
    result = calc.integrate(func, a, b, n=5000)
    print(f"∫_{a}^{b} {name} dx = {result:.8f}")
    
    # 特殊情況：arctan 積分
    if name == "1/(1+x²)":
        theoretical = math.atan(b) - math.atan(a)  # π/4
        print(f"  理論值: {theoretical:.8f} (π/4)")
```

## 進階使用案例

### 範例 9: 數值求根（結合微分）

```python
import math
from calculator import Calculator

def newton_raphson(calc, func, x0, tolerance=1e-8, max_iterations=100):
    """使用 Newton-Raphson 方法求根"""
    x = x0
    for i in range(max_iterations):
        fx = func(x)
        if abs(fx) < tolerance:
            return x, i
        
        # 使用數值微分計算導數
        fpx = calc.derivative(func, x)
        if abs(fpx) < 1e-15:
            raise ValueError("導數過小，無法繼續")
        
        x_new = x - fx / fpx
        if abs(x_new - x) < tolerance:
            return x_new, i
        x = x_new
    
    raise ValueError("超過最大迭代次數")

# 範例：求解 x³ - 2x - 1 = 0
calc = Calculator()
f = lambda x: x**3 - 2*x - 1

print("=== Newton-Raphson 求根範例 ===")
print("求解方程: x³ - 2x - 1 = 0")

try:
    root, iterations = newton_raphson(calc, f, 1.5)
    print(f"找到根: x = {root:.8f}")
    print(f"迭代次數: {iterations}")
    print(f"驗證: f({root:.8f}) = {f(root):.2e}")
except ValueError as e:
    print(f"求根失敗: {e}")
```

### 範例 10: 數值積分的蒙地卡羅方法

```python
import random
import math
from calculator import Calculator

def monte_carlo_integration(func, a, b, n_samples=100000):
    """使用蒙地卡羅方法計算積分"""
    total = 0
    for _ in range(n_samples):
        x = random.uniform(a, b)
        total += func(x)
    
    return (b - a) * total / n_samples

# 比較數值積分方法
calc = Calculator()
f = lambda x: math.sin(x) * math.exp(-x)

a, b = 0, math.pi
print("=== 積分方法比較 ===")
print(f"函數: f(x) = sin(x)·e^(-x), 區間: [0, π]")

# Simpson 法則
simpson_result = calc.integrate(f, a, b, method='simpson', n=10000)
print(f"Simpson 法則: {simpson_result:.8f}")

# 蒙地卡羅方法
random.seed(42)  # 確保可重現性
monte_carlo_result = monte_carlo_integration(f, a, b)
print(f"蒙地卡羅方法: {monte_carlo_result:.8f}")

print(f"差異: {abs(simpson_result - monte_carlo_result):.8f}")
```

## 錯誤處理

### 常見錯誤和處理方式

```python
from calculator import Calculator

calc = Calculator()

print("=== 錯誤處理範例 ===")

# 1. 除零錯誤
try:
    result = calc.divide(10, 0)
except ValueError as e:
    print(f"除零錯誤: {e}")

# 2. 無效的運算符號
try:
    result = calc.calculate('%', 10, 3)
except ValueError as e:
    print(f"無效運算符: {e}")

# 3. 微分方法錯誤
try:
    f = lambda x: x**2
    result = calc.derivative(f, 1.0, method='invalid_method')
except ValueError as e:
    print(f"微分方法錯誤: {e}")

# 4. 積分區間錯誤
try:
    f = lambda x: x**2
    result = calc.integrate(f, 5, 1)  # 上限小於下限
except ValueError as e:
    print(f"積分區間錯誤: {e}")

# 5. 函數評估錯誤
try:
    f = lambda x: math.log(x)  # log(x) 在 x <= 0 時未定義
    result = calc.integrate(f, -1, 1)
except ValueError as e:
    print(f"函數評估錯誤: {e}")
```

### 建議的錯誤處理模式

```python
from calculator import Calculator
import math

def safe_calculation(calc, operation, *args, **kwargs):
    """安全的計算包裝器"""
    try:
        if operation == 'derivative':
            return calc.derivative(*args, **kwargs)
        elif operation == 'integrate':
            return calc.integrate(*args, **kwargs)
        elif operation in ['+', '-', '*', '/']:
            return calc.calculate(operation, *args)
        else:
            raise ValueError(f"不支援的運算: {operation}")
    except ValueError as e:
        print(f"計算錯誤: {e}")
        return None
    except Exception as e:
        print(f"未預期的錯誤: {e}")
        return None

# 使用範例
calc = Calculator()

# 安全的微分計算
result = safe_calculation(calc, 'derivative', math.sin, math.pi/4)
if result is not None:
    print(f"sin'(π/4) = {result:.6f}")

# 安全的積分計算
f = lambda x: 1/x if x != 0 else float('inf')
result = safe_calculation(calc, 'integrate', f, 0.1, 2)
if result is not None:
    print(f"積分結果: {result:.6f}")
```

## 性能優化建議

### 1. 選擇適當的參數

```python
from calculator import Calculator
import time

calc = Calculator()

# 微分性能測試
f = lambda x: x**3 + 2*x**2 - x + 1

print("=== 微分性能比較 ===")
methods = ['central', 'five_point']
step_sizes = [1e-4, 1e-5, 1e-6, 1e-8]

for method in methods:
    print(f"\n{method.capitalize()} 方法:")
    for h in step_sizes:
        start_time = time.time()
        result = calc.derivative(f, 2.0, h=h, method=method)
        end_time = time.time()
        print(f"  h={h:.0e}: 結果={result:.8f}, 時間={end_time-start_time:.6f}s")
```

### 2. 積分精度與速度權衡

```python
import math
import time
from calculator import Calculator

calc = Calculator()

f = lambda x: math.sin(x) * math.exp(-x)

print("=== 積分性能比較 ===")
methods = ['trapezoidal', 'simpson']
n_values = [100, 1000, 5000, 10000]

for method in methods:
    print(f"\n{method.capitalize()} 方法:")
    for n in n_values:
        start_time = time.time()
        result = calc.integrate(f, 0, math.pi, n=n, method=method)
        end_time = time.time()
        print(f"  n={n:5d}: 結果={result:.8f}, 時間={end_time-start_time:.6f}s")
```

### 3. 批次處理

```python
from calculator import Calculator
import math

def batch_derivative(calc, func, points, **kwargs):
    """批次計算多個點的導數"""
    results = []
    for x in points:
        try:
            result = calc.derivative(func, x, **kwargs)
            results.append((x, result))
        except ValueError as e:
            results.append((x, None))
    return results

def batch_integrate(calc, func_list, **kwargs):
    """批次計算多個函數的積分"""
    results = []
    for func, a, b, label in func_list:
        try:
            result = calc.integrate(func, a, b, label=label, **kwargs)
            results.append((label, result))
        except ValueError as e:
            results.append((label, None))
    return results

# 使用範例
calc = Calculator()

print("=== 批次處理範例 ===")

# 批次微分
f = lambda x: x**3 - 2*x**2 + x - 1
points = [0, 0.5, 1, 1.5, 2]
derivatives = batch_derivative(calc, f, points)

print("批次微分結果:")
for x, result in derivatives:
    if result is not None:
        print(f"  f'({x}) = {result:.6f}")

# 批次積分
functions = [
    (lambda x: x**2, 0, 2, "x²"),
    (math.sin, 0, math.pi, "sin(x)"),
    (lambda x: math.exp(-x), 0, 2, "e^(-x)"),
]

integrals = batch_integrate(calc, functions)

print("\n批次積分結果:")
for label, result in integrals:
    if result is not None:
        print(f"  ∫ {label} dx = {result:.6f}")
```

---

## 總結

本 API 文檔提供了計算機專案的完整使用指南，包括：

- **基本運算**：四則運算和統一介面
- **數值微分**：兩種精度的微分方法
- **數值積分**：Simpson 和梯形法則
- **歷史管理**：運算記錄的儲存和管理
- **錯誤處理**：完整的異常處理機制
- **性能優化**：參數調整和批次處理建議

通過這些範例和說明，開發者可以快速掌握計算機的各項功能，並在自己的專案中有效運用。

如有任何問題或建議，歡迎提出討論！
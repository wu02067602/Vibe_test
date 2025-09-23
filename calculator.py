"""
計算機模組
提供基本的加減乘除運算功能
"""

from typing import Callable, Optional

class Calculator:
    """計算機類別，提供基本的數學運算功能"""
    
    def __init__(self):
        """初始化計算機"""
        self.history = []  # 儲存運算歷史
    
    def add(self, a, b):
        """加法運算"""
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def subtract(self, a, b):
        """減法運算"""
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        return result
    
    def multiply(self, a, b):
        """乘法運算"""
        result = a * b
        self.history.append(f"{a} × {b} = {result}")
        return result
    
    def divide(self, a, b):
        """除法運算"""
        if b == 0:
            raise ValueError("除數不能為零")
        result = a / b
        self.history.append(f"{a} ÷ {b} = {result}")
        return result
    
    def get_history(self):
        """取得運算歷史"""
        return self.history
    
    def clear_history(self):
        """清除運算歷史"""
        self.history.clear()
    
    def calculate(self, operation, a, b):
        """根據運算符號執行相應的運算"""
        if operation == '+':
            return self.add(a, b)
        elif operation == '-':
            return self.subtract(a, b)
        elif operation == '*':
            return self.multiply(a, b)
        elif operation == '/':
            return self.divide(a, b)
        else:
            raise ValueError(f"不支援的運算符號: {operation}")

    def derivative(self, func: Callable[[float], float], x: float, h: float = 1e-5,
                   method: str = 'five_point', label: Optional[str] = None) -> float:
        """數值微分

        使用數值方法估計函數在 x 的一階導數。

        參數:
            func: 可呼叫物件，輸入浮點數 x，回傳 f(x)
            x: 評估導數的位置
            h: 微小步長，預設 1e-5
            method: 使用的方法，'central' 或 'five_point'，預設 'five_point'
            label: 歷史紀錄中用來描述函數的標籤（例如表達式字串）

        回傳:
            在 x 的導數近似值
        """
        if h <= 0:
            raise ValueError("步長 h 必須為正數")

        try:
            if method == 'central':
                # 二點中央差分 O(h^2)
                result = (func(x + h) - func(x - h)) / (2.0 * h)
            elif method == 'five_point':
                # 五點中央差分 O(h^4)
                result = (
                    func(x - 2.0 * h)
                    - 8.0 * func(x - 1.0 * h)
                    + 8.0 * func(x + 1.0 * h)
                    - func(x + 2.0 * h)
                ) / (12.0 * h)
            else:
                raise ValueError("不支援的數值微分方法")
        except Exception as exc:
            raise ValueError(f"函數評估失敗: {exc}") from exc

        label_text = label if label else "f(x)"
        self.history.append(f"微分: d/dx [{label_text}] | x={x} ≈ {result}")
        return result
"""
計算機模組 (Calculator Module)
============================

這個模組提供了一個完整的計算機類別，支援：
- 基本四則運算（加、減、乘、除）
- 數值微分（中央差分法、五點中央差分法）
- 數值積分（Simpson 法則、梯形法則）
- 運算歷史記錄功能

作者：AI Assistant
版本：1.1.0
創建日期：2024
最後更新：2024

使用範例：
    >>> from calculator import Calculator
    >>> calc = Calculator()
    >>> result = calc.add(2, 3)
    >>> print(result)  # 輸出: 5
    >>> 
    >>> # 數值積分範例
    >>> import math
    >>> result = calc.integrate(math.sin, 0, math.pi)
    >>> print(result)  # 輸出: 約 2.0
"""

from typing import Callable, Optional

class Calculator:
    """
    計算機類別 - 提供完整的數學運算功能
    =====================================
    
    這個類別實現了一個功能豐富的計算機，包含：
    1. 基本四則運算
    2. 數值微分計算
    3. 數值積分計算
    4. 運算歷史管理
    
    屬性：
        history (list): 儲存所有運算記錄的列表
    
    範例：
        >>> calc = Calculator()
        >>> result = calc.calculate('+', 10, 5)
        >>> print(result)  # 15
        >>> history = calc.get_history()
        >>> print(history)  # ['10 + 5 = 15']
    """
    
    def __init__(self):
        """
        初始化計算機實例
        
        建立一個新的計算機物件，並初始化空的運算歷史記錄。
        """
        self.history = []  # 儲存運算歷史記錄的列表
    
    def add(self, a: float, b: float) -> float:
        """
        執行加法運算
        
        參數:
            a (float): 第一個加數
            b (float): 第二個加數
            
        回傳:
            float: 兩數相加的結果
            
        範例:
            >>> calc = Calculator()
            >>> result = calc.add(3.5, 2.1)
            >>> print(result)  # 5.6
        """
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def subtract(self, a: float, b: float) -> float:
        """
        執行減法運算
        
        參數:
            a (float): 被減數
            b (float): 減數
            
        回傳:
            float: 兩數相減的結果
            
        範例:
            >>> calc = Calculator()
            >>> result = calc.subtract(10, 3)
            >>> print(result)  # 7
        """
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        return result
    
    def multiply(self, a: float, b: float) -> float:
        """
        執行乘法運算
        
        參數:
            a (float): 第一個乘數
            b (float): 第二個乘數
            
        回傳:
            float: 兩數相乘的結果
            
        範例:
            >>> calc = Calculator()
            >>> result = calc.multiply(4, 2.5)
            >>> print(result)  # 10.0
        """
        result = a * b
        self.history.append(f"{a} × {b} = {result}")
        return result
    
    def divide(self, a: float, b: float) -> float:
        """
        執行除法運算
        
        參數:
            a (float): 被除數
            b (float): 除數
            
        回傳:
            float: 兩數相除的結果
            
        拋出:
            ValueError: 當除數為零時
            
        範例:
            >>> calc = Calculator()
            >>> result = calc.divide(15, 3)
            >>> print(result)  # 5.0
            >>> 
            >>> # 除零錯誤
            >>> calc.divide(10, 0)  # 拋出 ValueError
        """
        if b == 0:
            raise ValueError("除數不能為零")
        result = a / b
        self.history.append(f"{a} ÷ {b} = {result}")
        return result
    
    def get_history(self) -> list[str]:
        """
        取得所有運算歷史記錄
        
        回傳:
            list[str]: 包含所有運算記錄的列表，每個元素都是一個運算的字串表示
            
        範例:
            >>> calc = Calculator()
            >>> calc.add(2, 3)
            >>> calc.multiply(4, 5)
            >>> history = calc.get_history()
            >>> print(history)
            # ['2 + 3 = 5', '4 × 5 = 20']
        """
        return self.history
    
    def clear_history(self) -> None:
        """
        清除所有運算歷史記錄
        
        清除後，歷史列表將變為空列表。
        
        範例:
            >>> calc = Calculator()
            >>> calc.add(1, 2)
            >>> print(len(calc.get_history()))  # 1
            >>> calc.clear_history()
            >>> print(len(calc.get_history()))  # 0
        """
        self.history.clear()
    
    def calculate(self, operation: str, a: float, b: float) -> float:
        """
        根據運算符號執行相應的運算
        
        這是一個統一的運算介面，根據提供的運算符號自動選擇正確的運算方法。
        
        參數:
            operation (str): 運算符號，支援 '+', '-', '*', '/'
            a (float): 第一個運算數
            b (float): 第二個運算數
            
        回傳:
            float: 運算結果
            
        拋出:
            ValueError: 當運算符號不支援或除數為零時
            
        範例:
            >>> calc = Calculator()
            >>> result = calc.calculate('+', 10, 5)
            >>> print(result)  # 15.0
            >>> result = calc.calculate('/', 20, 4)
            >>> print(result)  # 5.0
        """
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
        """
        計算數值微分（一階導數）
        
        使用數值方法估計函數在指定點的一階導數。支援兩種數值微分方法：
        1. 中央差分法：精度 O(h²)，計算較快
        2. 五點中央差分法：精度 O(h⁴)，精度較高
        
        數學原理：
        - 中央差分：f'(x) ≈ [f(x+h) - f(x-h)] / (2h)
        - 五點中央差分：f'(x) ≈ [f(x-2h) - 8f(x-h) + 8f(x+h) - f(x+2h)] / (12h)

        參數:
            func (Callable[[float], float]): 要微分的函數，必須接受一個浮點數參數並回傳浮點數
            x (float): 計算導數的點
            h (float, optional): 微小步長，用於數值近似。預設為 1e-5
            method (str, optional): 數值方法，'central' 或 'five_point'。預設為 'five_point'
            label (Optional[str], optional): 函數的描述標籤，用於歷史記錄。預設為 None

        回傳:
            float: 函數在 x 點的導數近似值

        拋出:
            ValueError: 當步長 h <= 0 或方法不支援時
            ValueError: 當函數評估失敗時

        範例:
            >>> import math
            >>> calc = Calculator()
            >>> # 計算 x² 在 x=2 的導數（理論值為 4）
            >>> f = lambda x: x**2
            >>> result = calc.derivative(f, 2.0)
            >>> print(f"{result:.6f}")  # 約 4.000000
            >>> 
            >>> # 計算 sin(x) 在 x=0 的導數（理論值為 1）
            >>> result = calc.derivative(math.sin, 0.0, method='central')
            >>> print(f"{result:.6f}")  # 約 1.000000
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

    def integrate(self, func: Callable[[float], float], a: float, b: float, 
                  n: int = 1000, method: str = 'simpson', 
                  label: Optional[str] = None) -> float:
        """
        計算數值積分（定積分）
        
        使用數值方法估計函數在指定區間的定積分。支援兩種數值積分方法：
        1. 梯形法則：將積分區間分割為梯形，計算較快
        2. Simpson 法則（1/3 法則）：使用拋物線近似，精度較高
        
        數學原理：
        - 梯形法則：∫f(x)dx ≈ (h/2)[f(a) + 2∑f(xi) + f(b)]
        - Simpson 法則：∫f(x)dx ≈ (h/3)[f(a) + 4∑f(x_odd) + 2∑f(x_even) + f(b)]
        
        其中 h = (b-a)/n 為步長，xi 為分割點。

        參數:
            func (Callable[[float], float]): 要積分的函數，必須接受一個浮點數參數並回傳浮點數
            a (float): 積分下限
            b (float): 積分上限
            n (int, optional): 分割數量，Simpson 法則需要偶數。預設為 1000
            method (str, optional): 數值方法，'trapezoidal' 或 'simpson'。預設為 'simpson'
            label (Optional[str], optional): 函數的描述標籤，用於歷史記錄。預設為 None
            
        回傳:
            float: 函數在區間 [a, b] 的積分近似值

        拋出:
            ValueError: 當 a >= b（無效積分區間）時
            ValueError: 當 n <= 0（無效分割數量）時
            ValueError: 當積分方法不支援時
            ValueError: 當函數評估失敗時

        範例:
            >>> import math
            >>> calc = Calculator()
            >>> # 計算 x² 從 0 到 3 的積分（理論值為 9）
            >>> f = lambda x: x**2
            >>> result = calc.integrate(f, 0, 3)
            >>> print(f"{result:.6f}")  # 約 9.000000
            >>> 
            >>> # 計算 sin(x) 從 0 到 π 的積分（理論值為 2）
            >>> result = calc.integrate(math.sin, 0, math.pi, method='trapezoidal')
            >>> print(f"{result:.6f}")  # 約 2.000000
            >>>
            >>> # 使用更多分割點提高精度
            >>> result = calc.integrate(f, 0, 1, n=10000)
            >>> print(f"{result:.8f}")  # 更精確的結果
        """
        if a >= b:
            raise ValueError("積分上限必須大於下限")
        if n <= 0:
            raise ValueError("分割數量必須為正整數")
        if method == 'simpson' and n % 2 != 0:
            n += 1  # Simpson 法則需要偶數個分割點，自動調整
            
        try:
            # 計算步長
            h = (b - a) / n
            
            if method == 'trapezoidal':
                # 梯形法則實現
                # 第一項和最後一項各乘以 0.5，中間項乘以 1
                result = 0.5 * (func(a) + func(b))
                
                # 計算中間點的函數值總和
                for i in range(1, n):
                    x = a + i * h
                    result += func(x)
                
                # 乘以步長得到最終結果
                result *= h
                
            elif method == 'simpson':
                # Simpson 法則（1/3 法則）實現
                # 端點函數值
                result = func(a) + func(b)
                
                # 奇數索引點（x1, x3, x5, ...）的係數為 4
                for i in range(1, n, 2):
                    x = a + i * h
                    result += 4 * func(x)
                
                # 偶數索引點（x2, x4, x6, ...）的係數為 2
                for i in range(2, n, 2):
                    x = a + i * h
                    result += 2 * func(x)
                
                # 乘以 h/3 得到最終結果
                result *= h / 3
                
            else:
                raise ValueError("不支援的數值積分方法")
                
        except Exception as exc:
            raise ValueError(f"函數評估失敗: {exc}") from exc
        
        label_text = label if label else "f(x)"
        self.history.append(f"積分: ∫ [{label_text}] dx 從 {a} 到 {b} ≈ {result}")
        return result
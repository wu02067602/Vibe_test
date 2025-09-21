"""
計算機模組
提供基本的加減乘除運算功能
"""

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
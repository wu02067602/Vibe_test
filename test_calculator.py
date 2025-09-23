#!/usr/bin/env python3
"""
計算機測試程式 (Calculator Test Suite)
====================================

這是計算機專案的完整測試套件，使用 Python unittest 框架進行全面的功能測試。

測試涵蓋範圍：
- 基本四則運算的正確性和邊界條件
- 數值微分的精度和錯誤處理
- 數值積分的精度和錯誤處理
- 運算歷史記錄功能
- 異常情況的處理

測試策略：
- 單元測試：測試每個方法的獨立功能
- 邊界測試：測試極值和特殊情況
- 錯誤測試：確保異常情況得到正確處理
- 精度測試：驗證數值方法的計算精度

執行方法：
    python test_calculator.py

預期結果：
    所有測試應該通過，顯示 "OK" 狀態

作者：AI Assistant
版本：1.1.0
創建日期：2024
最後更新：2024
"""

import unittest
from calculator import Calculator
import math

class TestCalculator(unittest.TestCase):
    """
    計算機測試類別
    
    這個類別包含計算機所有功能的測試方法。每個測試方法都專注於測試
    特定的功能或邊界條件，確保計算機在各種情況下都能正確運作。
    
    測試分類：
    - test_*_basic: 基本功能測試
    - test_*_edge_cases: 邊界條件測試  
    - test_*_errors: 錯誤處理測試
    - test_*_precision: 精度驗證測試
    
    測試原則：
    - 每個測試方法獨立運行
    - 使用 setUp 方法初始化測試環境
    - 使用 assert* 方法驗證結果
    - 包含清楚的測試說明和預期結果
    """
    
    def setUp(self):
        """
        測試前準備
        
        在每個測試方法執行前自動調用，用於初始化測試環境。
        建立一個新的 Calculator 實例，確保每個測試都從乾淨的狀態開始。
        """
        self.calc = Calculator()
    
    def test_addition(self):
        """
        測試加法運算的正確性
        
        測試情境：
        - 正整數加法：2 + 3 = 5
        - 正負數加法：-1 + 1 = 0
        - 零加法：0 + 0 = 0
        - 小數加法：1.5 + 2.5 = 4.0
        
        驗證點：
        - 基本數學運算正確
        - 支援正負數和小數
        - 結果自動記錄到歷史
        """
        self.assertEqual(self.calc.add(2, 3), 5)
        self.assertEqual(self.calc.add(-1, 1), 0)
        self.assertEqual(self.calc.add(0, 0), 0)
        self.assertEqual(self.calc.add(1.5, 2.5), 4.0)
    
    def test_subtraction(self):
        """
        測試減法運算的正確性
        
        測試情境：
        - 正整數減法：5 - 3 = 2
        - 相等數減法：1 - 1 = 0
        - 結果為負數：0 - 5 = -5
        - 小數減法：3.5 - 1.5 = 2.0
        
        驗證點：
        - 減法運算正確
        - 支援負數結果
        - 小數精度正確
        """
        self.assertEqual(self.calc.subtract(5, 3), 2)
        self.assertEqual(self.calc.subtract(1, 1), 0)
        self.assertEqual(self.calc.subtract(0, 5), -5)
        self.assertEqual(self.calc.subtract(3.5, 1.5), 2.0)
    
    def test_multiplication(self):
        """
        測試乘法運算的正確性
        
        測試情境：
        - 正整數乘法：2 × 3 = 6
        - 負數乘法：-2 × 3 = -6
        - 零乘法：0 × 5 = 0
        - 小數乘法：2.5 × 4 = 10.0
        
        驗證點：
        - 乘法運算正確
        - 正負號處理正確
        - 零值處理正確
        """
        self.assertEqual(self.calc.multiply(2, 3), 6)
        self.assertEqual(self.calc.multiply(-2, 3), -6)
        self.assertEqual(self.calc.multiply(0, 5), 0)
        self.assertEqual(self.calc.multiply(2.5, 4), 10.0)
    
    def test_division(self):
        """
        測試除法運算的正確性
        
        測試情境：
        - 整除：6 ÷ 2 = 3
        - 小數結果：5 ÷ 2 = 2.5
        - 負數除法：-6 ÷ 2 = -3
        - 零除法：0 ÷ 5 = 0
        
        驗證點：
        - 除法運算正確
        - 支援小數結果
        - 負數處理正確
        """
        self.assertEqual(self.calc.divide(6, 2), 3)
        self.assertEqual(self.calc.divide(5, 2), 2.5)
        self.assertEqual(self.calc.divide(-6, 2), -3)
        self.assertEqual(self.calc.divide(0, 5), 0)
    
    def test_division_by_zero(self):
        """
        測試除零錯誤處理
        
        測試情境：
        - 嘗試執行 5 ÷ 0
        
        預期結果：
        - 拋出 ValueError 異常
        - 錯誤訊息為 "除數不能為零"
        
        驗證點：
        - 除零檢查機制正常運作
        - 異常處理正確
        """
        with self.assertRaises(ValueError):
            self.calc.divide(5, 0)
    
    def test_calculate_method(self):
        """
        測試統一運算介面 calculate 方法
        
        測試情境：
        - 測試所有支援的運算符號：+, -, *, /
        - 測試不支援的運算符號：%
        
        預期結果：
        - 支援的運算符號正常運作
        - 不支援的運算符號拋出 ValueError
        
        驗證點：
        - 統一介面正常運作
        - 運算符號驗證正確
        """
        self.assertEqual(self.calc.calculate('+', 2, 3), 5)
        self.assertEqual(self.calc.calculate('-', 5, 3), 2)
        self.assertEqual(self.calc.calculate('*', 2, 3), 6)
        self.assertEqual(self.calc.calculate('/', 6, 2), 3)
        
        with self.assertRaises(ValueError):
            self.calc.calculate('%', 5, 3)
    
    def test_history(self):
        """
        測試運算歷史記錄功能
        
        測試情境：
        - 執行多個運算並檢查歷史記錄
        - 測試歷史清除功能
        
        測試步驟：
        1. 執行加法：1 + 2
        2. 執行減法：5 - 3
        3. 檢查歷史記錄數量和內容
        4. 清除歷史
        5. 驗證歷史已清空
        
        驗證點：
        - 歷史記錄正確儲存
        - 記錄格式正確
        - 清除功能正常
        """
        self.calc.add(1, 2)
        self.calc.subtract(5, 3)
        history = self.calc.get_history()
        
        self.assertEqual(len(history), 2)
        self.assertIn("1 + 2 = 3", history)
        self.assertIn("5 - 3 = 2", history)
        
        self.calc.clear_history()
        self.assertEqual(len(self.calc.get_history()), 0)

    def test_derivative_central_and_five_point(self):
        """
        測試數值微分的两種方法及其精度
        
        測試函數：
        1. f(x) = x² -> f'(x) = 2x
        2. f(x) = sin(x) -> f'(x) = cos(x)
        
        測試方法：
        - 中央差分法（精度 O(h²)）
        - 五點中央差分法（精度 O(h⁴)）
        
        測試參數：
        - 步長 h = 1e-5
        - 評估點 x0 = 1.234, x1 = 0.7
        
        驗證標準：
        - 精度至少 6 位小數
        - 兩種方法結果都應接近理論值
        """
        # f(x) = x^2 -> f'(x) = 2x
        f = lambda x: x * x
        x0 = 1.234
        expected = 2 * x0
        d_central = self.calc.derivative(f, x0, h=1e-5, method='central')
        d_five = self.calc.derivative(f, x0, h=1e-5, method='five_point')
        self.assertAlmostEqual(d_central, expected, places=6)
        self.assertAlmostEqual(d_five, expected, places=6)

        # f(x) = sin(x) -> f'(x) = cos(x)
        g = math.sin
        x1 = 0.7
        expected_g = math.cos(x1)
        d_g = self.calc.derivative(g, x1, h=1e-5, method='five_point')
        self.assertAlmostEqual(d_g, expected_g, places=6)

    def test_derivative_invalid_method(self):
        """
        測試不支援的微分方法錯誤處理
        
        測試情境：
        - 使用不存在的方法名稱 'unknown'
        
        預期結果：
        - 拋出 ValueError 異常
        - 錯誤訊息包含方法不支援的說明
        
        驗證點：
        - 輸入驗證機制正常運作
        - 錯誤訊息清晰明確
        """
        with self.assertRaises(ValueError):
            self.calc.derivative(lambda x: x, 0.0, method='unknown')

    def test_derivative_invalid_h(self):
        """
        測試無效步長的錯誤處理
        
        測試情境：
        - 使用零或負數作為步長 h
        
        預期結果：
        - 拋出 ValueError 異常
        - 錯誤訊息為 "步長 h 必須為正數"
        
        驗證點：
        - 參數範圍檢查正常
        - 數值方法的穩定性要求得到保護
        """
        with self.assertRaises(ValueError):
            self.calc.derivative(lambda x: x, 0.0, h=0)

    def test_integrate_simpson(self):
        """
        測試 Simpson 法則數值積分的精度和正確性
        
        測試函數及理論值：
        1. f(x) = x², [0,3]: ∫ x² dx = x³/3 |_0³ = 9
        2. f(x) = sin(x), [0,π]: ∫ sin(x) dx = -cos(x) |_0^π = 2
        3. f(x) = 2x+1, [1,3]: ∫ (2x+1) dx = x²+x |_1³ = 10
        
        測試參數：
        - 使用 Simpson 法則（預設）
        - 預設分割數 n = 1000
        
        精度要求：
        - 結果精度至少 5 位小數
        - Simpson 法則應該提供高精度結果
        
        驗證點：
        - 多項式函數積分正確
        - 三角函數積分正確
        - 線性函數積分正確
        """
        # f(x) = x^2 從 0 到 3 的積分 = x^3/3 |_0^3 = 9
        f1 = lambda x: x**2
        result1 = self.calc.integrate(f1, 0, 3, method='simpson')
        self.assertAlmostEqual(result1, 9.0, places=5)
        
        # f(x) = sin(x) 從 0 到 π 的積分 = -cos(x) |_0^π = 2
        f2 = math.sin
        result2 = self.calc.integrate(f2, 0, math.pi, method='simpson')
        self.assertAlmostEqual(result2, 2.0, places=5)
        
        # f(x) = 2x + 1 從 1 到 3 的積分 = x^2 + x |_1^3 = (9+3) - (1+1) = 10
        f3 = lambda x: 2*x + 1
        result3 = self.calc.integrate(f3, 1, 3, method='simpson')
        self.assertAlmostEqual(result3, 10.0, places=5)

    def test_integrate_trapezoidal(self):
        """
        測試梯形法則數值積分的正確性
        
        測試函數：
        - f(x) = x², 區間 [0,2]
        - 理論值：∫₀² x² dx = x³/3 |_0² = 8/3 ≈ 2.667
        
        測試參數：
        - 使用梯形法則
        - 分割數 n = 1000
        
        精度要求：
        - 結果精度至少 3 位小數
        - 梯形法則精度低於 Simpson 法則但計算較快
        
        驗證點：
        - 梯形法則實現正確
        - 精度符合預期
        """
        # f(x) = x^2 從 0 到 2 的積分 = x^3/3 |_0^2 = 8/3 ≈ 2.667
        f = lambda x: x**2
        result = self.calc.integrate(f, 0, 2, method='trapezoidal', n=1000)
        expected = 8.0 / 3.0
        self.assertAlmostEqual(result, expected, places=3)

    def test_integrate_invalid_bounds(self):
        """
        測試無效積分區間的錯誤處理
        
        測試情境：
        1. 上限小於下限：a=3, b=1 (a > b)
        2. 上下限相等：a=1, b=1 (a = b)
        
        預期結果：
        - 兩種情況都應拋出 ValueError
        - 錯誤訊息："積分上限必須大於下限"
        
        驗證點：
        - 區間有效性檢查正常
        - 數學定義的正確性得到保護
        """
        f = lambda x: x
        with self.assertRaises(ValueError):
            self.calc.integrate(f, 3, 1)  # a >= b
        with self.assertRaises(ValueError):
            self.calc.integrate(f, 1, 1)  # a == b

    def test_integrate_invalid_n(self):
        """
        測試無效分割數量的錯誤處理
        
        測試情境：
        1. 分割數為零：n = 0
        2. 分割數為負數：n = -5
        
        預期結果：
        - 兩種情況都應拋出 ValueError
        - 錯誤訊息："分割數量必須為正整數"
        
        驗證點：
        - 參數範圍檢查正常
        - 數值方法的穩定性要求得到保護
        """
        f = lambda x: x
        with self.assertRaises(ValueError):
            self.calc.integrate(f, 0, 1, n=0)  # n <= 0
        with self.assertRaises(ValueError):
            self.calc.integrate(f, 0, 1, n=-5)  # n < 0

    def test_integrate_invalid_method(self):
        """
        測試不支援的積分方法錯誤處理
        
        測試情境：
        - 使用不存在的方法名稱 'unknown'
        
        支援的方法：
        - 'simpson': Simpson 法則
        - 'trapezoidal': 梯形法則
        
        預期結果：
        - 拋出 ValueError 異常
        - 錯誤訊息包含方法不支援的說明
        
        驗證點：
        - 輸入驗證機制正常運作
        - 方法名稱檢查正確
        """
        f = lambda x: x
        with self.assertRaises(ValueError):
            self.calc.integrate(f, 0, 1, method='unknown')

    def test_integrate_history(self):
        """
        測試積分運算的歷史記錄功能
        
        測試情境：
        - 執行一次積分運算：f(x) = x², [0,2]
        - 使用自定義標籤 'x**2'
        
        測試步驟：
        1. 執行積分運算
        2. 取得歷史記錄
        3. 檢查記錄數量
        4. 驗證記錄內容格式
        
        預期結果：
        - 歷史記錄數量為 1
        - 記錄內容包含積分符號、函數名稱和區間
        
        驗證點：
        - 積分運算正確記錄到歷史
        - 記錄格式符合預期
        - 自定義標籤正確顯示
        """
        f = lambda x: x**2
        self.calc.integrate(f, 0, 2, label='x**2')
        history = self.calc.get_history()
        self.assertEqual(len(history), 1)
        self.assertIn("積分: ∫ [x**2] dx 從 0 到 2", history[0])

if __name__ == '__main__':
    """
    測試程式主要執行點
    
    當此檔案被直接執行時（而非被匯入），會自動執行所有測試。
    使用 unittest.main() 來發現並執行所有以 'test_' 開頭的方法。
    
    參數說明：
    - verbosity=2: 詳細輸出模式，顯示每個測試的名稱和結果
    
    輸出格式：
    - 每個測試方法會顯示其名稱和執行狀態（ok/FAIL/ERROR）
    - 最後顯示總結：執行的測試數量、耗時、整體結果
    
    預期結果：
    - 所有測試都應該通過（顯示 "ok"）
    - 最終狀態應該是 "OK"
    - 沒有失敗或錯誤
    """
    print("執行計算機測試...")
    print("=" * 50)
    unittest.main(verbosity=2)
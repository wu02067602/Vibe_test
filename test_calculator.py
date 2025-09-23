#!/usr/bin/env python3
"""
計算機測試程式
測試計算機的各項功能
"""

import unittest
from calculator import Calculator
import math

class TestCalculator(unittest.TestCase):
    """計算機測試類別"""
    
    def setUp(self):
        """測試前準備"""
        self.calc = Calculator()
    
    def test_addition(self):
        """測試加法"""
        self.assertEqual(self.calc.add(2, 3), 5)
        self.assertEqual(self.calc.add(-1, 1), 0)
        self.assertEqual(self.calc.add(0, 0), 0)
        self.assertEqual(self.calc.add(1.5, 2.5), 4.0)
    
    def test_subtraction(self):
        """測試減法"""
        self.assertEqual(self.calc.subtract(5, 3), 2)
        self.assertEqual(self.calc.subtract(1, 1), 0)
        self.assertEqual(self.calc.subtract(0, 5), -5)
        self.assertEqual(self.calc.subtract(3.5, 1.5), 2.0)
    
    def test_multiplication(self):
        """測試乘法"""
        self.assertEqual(self.calc.multiply(2, 3), 6)
        self.assertEqual(self.calc.multiply(-2, 3), -6)
        self.assertEqual(self.calc.multiply(0, 5), 0)
        self.assertEqual(self.calc.multiply(2.5, 4), 10.0)
    
    def test_division(self):
        """測試除法"""
        self.assertEqual(self.calc.divide(6, 2), 3)
        self.assertEqual(self.calc.divide(5, 2), 2.5)
        self.assertEqual(self.calc.divide(-6, 2), -3)
        self.assertEqual(self.calc.divide(0, 5), 0)
    
    def test_division_by_zero(self):
        """測試除零錯誤"""
        with self.assertRaises(ValueError):
            self.calc.divide(5, 0)
    
    def test_calculate_method(self):
        """測試 calculate 方法"""
        self.assertEqual(self.calc.calculate('+', 2, 3), 5)
        self.assertEqual(self.calc.calculate('-', 5, 3), 2)
        self.assertEqual(self.calc.calculate('*', 2, 3), 6)
        self.assertEqual(self.calc.calculate('/', 6, 2), 3)
        
        with self.assertRaises(ValueError):
            self.calc.calculate('%', 5, 3)
    
    def test_history(self):
        """測試運算歷史"""
        self.calc.add(1, 2)
        self.calc.subtract(5, 3)
        history = self.calc.get_history()
        
        self.assertEqual(len(history), 2)
        self.assertIn("1 + 2 = 3", history)
        self.assertIn("5 - 3 = 2", history)
        
        self.calc.clear_history()
        self.assertEqual(len(self.calc.get_history()), 0)

    def test_derivative_central_and_five_point(self):
        """測試微分（中央差分與五點中央）"""
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
        """測試不支援的微分方法"""
        with self.assertRaises(ValueError):
            self.calc.derivative(lambda x: x, 0.0, method='unknown')

    def test_derivative_invalid_h(self):
        """測試無效步長"""
        with self.assertRaises(ValueError):
            self.calc.derivative(lambda x: x, 0.0, h=0)

    def test_integrate_simpson(self):
        """測試 Simpson 法則積分"""
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
        """測試梯形法則積分"""
        # f(x) = x^2 從 0 到 2 的積分 = x^3/3 |_0^2 = 8/3 ≈ 2.667
        f = lambda x: x**2
        result = self.calc.integrate(f, 0, 2, method='trapezoidal', n=1000)
        expected = 8.0 / 3.0
        self.assertAlmostEqual(result, expected, places=3)

    def test_integrate_invalid_bounds(self):
        """測試無效的積分區間"""
        f = lambda x: x
        with self.assertRaises(ValueError):
            self.calc.integrate(f, 3, 1)  # a >= b
        with self.assertRaises(ValueError):
            self.calc.integrate(f, 1, 1)  # a == b

    def test_integrate_invalid_n(self):
        """測試無效的分割數量"""
        f = lambda x: x
        with self.assertRaises(ValueError):
            self.calc.integrate(f, 0, 1, n=0)  # n <= 0
        with self.assertRaises(ValueError):
            self.calc.integrate(f, 0, 1, n=-5)  # n < 0

    def test_integrate_invalid_method(self):
        """測試不支援的積分方法"""
        f = lambda x: x
        with self.assertRaises(ValueError):
            self.calc.integrate(f, 0, 1, method='unknown')

    def test_integrate_history(self):
        """測試積分歷史記錄"""
        f = lambda x: x**2
        self.calc.integrate(f, 0, 2, label='x**2')
        history = self.calc.get_history()
        self.assertEqual(len(history), 1)
        self.assertIn("積分: ∫ [x**2] dx 從 0 到 2", history[0])

if __name__ == '__main__':
    print("執行計算機測試...")
    unittest.main(verbosity=2)
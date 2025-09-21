#!/usr/bin/env python3
"""
計算機測試程式
測試計算機的各項功能
"""

import unittest
from calculator import Calculator

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

if __name__ == '__main__':
    print("執行計算機測試...")
    unittest.main(verbosity=2)
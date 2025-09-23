#!/usr/bin/env python3
"""
計算機主程式
提供命令列介面讓使用者進行計算
"""

import sys
import math
from calculator import Calculator

def display_menu():
    """顯示選單"""
    print("\n" + "="*40)
    print("           計算機")
    print("="*40)
    print("1. 加法 (+)")
    print("2. 減法 (-)")
    print("3. 乘法 (×)")
    print("4. 除法 (÷)")
    print("7. 微分 d/dx [輸入函數表達式]")
    print("5. 查看運算歷史")
    print("6. 清除歷史")
    print("0. 離開")
    print("="*40)

def get_number(prompt):
    """取得使用者輸入的數字"""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("請輸入有效的數字！")

def get_operation():
    """取得使用者選擇的運算"""
    while True:
        choice = input("請選擇運算 (1-4): ").strip()
        if choice in ['1', '2', '3', '4']:
            operations = {'1': '+', '2': '-', '3': '*', '4': '/'}
            return operations[choice]
        print("請輸入 1-4 之間的數字！")

def build_function_from_expr(expr: str):
    """從使用者輸入的表達式建立函數 f(x)

    支援 math 模組中的函數，例如: sin, cos, exp, log 等。
    範例輸入: x**2 + 3*x + 1,  sin(x) + x
    """
    # 準備允許使用的名稱
    allowed_names = {name: getattr(math, name) for name in dir(math) if not name.startswith('_')}

    def func(x):
        local_names = dict(allowed_names)
        local_names['x'] = x
        return eval(expr, {"__builtins__": {}}, local_names)

    return func

def main():
    """主程式"""
    calc = Calculator()
    
    print("歡迎使用計算機！")
    
    while True:
        display_menu()
        choice = input("請選擇功能 (0-7): ").strip()
        
        if choice == '0':
            print("感謝使用計算機，再見！")
            break
        elif choice == '5':
            # 查看運算歷史
            history = calc.get_history()
            if history:
                print("\n運算歷史：")
                for i, record in enumerate(history, 1):
                    print(f"{i}. {record}")
            else:
                print("尚無運算記錄")
        elif choice == '6':
            # 清除歷史
            calc.clear_history()
            print("運算歷史已清除")
        elif choice == '7':
            # 微分功能
            try:
                print("\n請輸入函數表達式，變數名稱為 x，例如: x**2 + 3*x + 1 或 sin(x)")
                expr = input("f(x) = ").strip()
                if not expr:
                    print("表達式不可為空！")
                    continue

                x = get_number("請輸入評估點 x: ")

                method_input = input("選擇數值方法 [1] 五點中央(預設)  [2] 中央差分: ").strip()
                method = 'five_point' if method_input in ['', '1'] else 'central'

                h_input = input("步長 h (預設 1e-5，直接 Enter 採預設): ").strip()
                h = 1e-5 if h_input == '' else float(h_input)

                f = build_function_from_expr(expr)
                result = calc.derivative(f, x, h=h, method=method, label=expr)
                print(f"\n結果: f'(x) 在 x={x} 的近似值為 {result}")
            except ValueError as e:
                print(f"錯誤: {e}")
            except Exception as e:
                print(f"錯誤: 無法解析或計算該表達式 ({e})")
        elif choice in ['1', '2', '3', '4']:
            # 執行運算
            try:
                operation = get_operation()
                if operation:
                    a = get_number("請輸入第一個數字: ")
                    b = get_number("請輸入第二個數字: ")
                    
                    result = calc.calculate(operation, a, b)
                    print(f"\n結果: {result}")
            except ValueError as e:
                print(f"錯誤: {e}")
        else:
            print("無效的選擇，請重新輸入！")
        
        input("\n按 Enter 鍵繼續...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程式被中斷，再見！")
        sys.exit(0)
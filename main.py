#!/usr/bin/env python3
"""
計算機主程式 (Calculator Main Program)
====================================

這是一個功能完整的命令列計算機應用程式，提供友善的使用者介面來執行各種數學運算。

主要功能：
- 基本四則運算（加、減、乘、除）
- 數值微分計算（支援多種數值方法）
- 數值積分計算（支援 Simpson 法則和梯形法則）
- 運算歷史記錄管理
- 支援數學函數表達式（sin, cos, exp, log 等）

技術特色：
- 完整的錯誤處理和輸入驗證
- 支援浮點數運算
- 靈活的函數表達式解析
- 安全的 eval 執行環境

使用方法：
    python main.py

作者：AI Assistant
版本：1.1.0
創建日期：2024
最後更新：2024

相依套件：
- math: Python 標準數學函數庫
- sys: 系統相關功能
- calculator: 自定義計算機模組
"""

import sys
import math
from calculator import Calculator

def display_menu() -> None:
    """
    顯示主選單介面
    
    在終端上顯示美觀的選單，列出所有可用的功能選項。
    選單包含基本運算、進階數學功能和系統管理功能。
    
    功能分類：
    - 基本運算：選項 1-4
    - 進階數學：選項 7-8
    - 系統管理：選項 5-6, 0
    """
    print("\n" + "="*40)
    print("           計算機")
    print("="*40)
    print("1. 加法 (+)")
    print("2. 減法 (-)")
    print("3. 乘法 (×)")
    print("4. 除法 (÷)")
    print("7. 微分 d/dx [輸入函數表達式]")
    print("8. 積分 ∫ [輸入函數表達式]")
    print("5. 查看運算歷史")
    print("6. 清除歷史")
    print("0. 離開")
    print("="*40)

def get_number(prompt: str) -> float:
    """
    取得使用者輸入的數字
    
    持續提示使用者輸入數字，直到輸入有效的數字為止。
    支援整數和浮點數輸入。
    
    參數：
        prompt (str): 顯示給使用者的提示訊息
        
    回傳：
        float: 使用者輸入的數字值
        
    範例：
        >>> number = get_number("請輸入一個數字: ")
        請輸入一個數字: 3.14
        >>> print(number)  # 3.14
    """
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("請輸入有效的數字！")

def get_operation() -> str:
    """
    取得使用者選擇的運算符號
    
    提示使用者選擇基本四則運算之一，直到輸入有效選項為止。
    將數字選項轉換為對應的運算符號。
    
    選項對應：
        1 -> '+' (加法)
        2 -> '-' (減法)
        3 -> '*' (乘法)
        4 -> '/' (除法)
        
    回傳：
        str: 運算符號字串 ('+', '-', '*', '/')
        
    範例：
        >>> op = get_operation()
        請選擇運算 (1-4): 1
        >>> print(op)  # '+'
    """
    while True:
        choice = input("請選擇運算 (1-4): ").strip()
        if choice in ['1', '2', '3', '4']:
            operations = {'1': '+', '2': '-', '3': '*', '4': '/'}
            return operations[choice]
        print("請輸入 1-4 之間的數字！")

def build_function_from_expr(expr: str) -> callable:
    """
    從使用者輸入的字串表達式建立可呼叫的數學函數
    
    這個函數提供安全的表達式評估環境，只允許使用 math 模組中的函數和變數 x。
    透過限制 __builtins__ 來防止執行危險的程式碼。
    
    支援的數學函數包括：
    - 基本函數：sin, cos, tan, asin, acos, atan, atan2
    - 雙曲函數：sinh, cosh, tanh
    - 指數和對數：exp, log, log10, log2, pow, sqrt
    - 常數：pi, e
    - 其他：ceil, floor, fabs, factorial 等
    
    參數：
        expr (str): 數學表達式字串，變數必須使用 'x'
        
    回傳：
        callable: 接受一個數值參數 x 並回傳計算結果的函數
        
    拋出：
        可能的異常會在函數被呼叫時產生，包括：
        - NameError: 使用了不允許的變數或函數名稱
        - SyntaxError: 表達式語法錯誤
        - TypeError: 類型錯誤
        - ValueError: 數值錯誤（如 log 負數）
        
    範例：
        >>> f = build_function_from_expr("x**2 + 3*x + 1")
        >>> result = f(2)  # 計算 2² + 3×2 + 1 = 11
        >>> print(result)  # 11
        >>>
        >>> g = build_function_from_expr("sin(x) + cos(x)")
        >>> result = g(0)  # 計算 sin(0) + cos(0) = 1
        >>> print(result)  # 1.0
        >>>
        >>> h = build_function_from_expr("exp(x) * log(x)")
        >>> result = h(1)  # 計算 e¹ × ln(1) = 0
        >>> print(result)  # 0.0
        
    安全性說明：
        - 禁用所有內建函數，防止執行 open(), exec() 等危險操作
        - 只允許 math 模組中的函數和常數
        - 只允許變數 'x'，防止存取其他變數
    """
    # 準備允許使用的名稱：包含 math 模組中所有非私有成員
    allowed_names = {name: getattr(math, name) for name in dir(math) if not name.startswith('_')}

    def func(x: float) -> float:
        """
        內部函數：評估表達式
        
        參數：
            x (float): 函數的輸入值
            
        回傳：
            float: 表達式的計算結果
        """
        # 建立局部命名空間，包含 math 函數和變數 x
        local_names = dict(allowed_names)
        local_names['x'] = x
        
        # 在安全環境中評估表達式
        return eval(expr, {"__builtins__": {}}, local_names)

    return func

def main() -> None:
    """
    主程式函數 - 計算機應用程式的入口點
    
    這個函數實現了計算機的主要執行邏輯，包括：
    1. 初始化計算機實例
    2. 顯示歡迎訊息
    3. 進入主要的使用者互動迴圈
    4. 處理各種功能選項
    5. 提供完整的錯誤處理
    
    程式流程：
    - 顯示主選單
    - 接受使用者選擇
    - 根據選擇執行對應功能
    - 顯示結果或錯誤訊息
    - 等待使用者確認後繼續
    
    支援的功能：
    - 基本四則運算 (選項 1-4)
    - 查看和管理運算歷史 (選項 5-6)
    - 數值微分計算 (選項 7)
    - 數值積分計算 (選項 8)
    - 程式結束 (選項 0)
    
    異常處理：
    - ValueError: 數值輸入錯誤、運算錯誤
    - KeyboardInterrupt: 使用者中斷程式
    - Exception: 其他未預期的錯誤
    """
    # 初始化計算機實例
    calc = Calculator()
    
    # 顯示歡迎訊息
    print("歡迎使用計算機！")
    
    # 主要互動迴圈
    while True:
        display_menu()
        choice = input("請選擇功能 (0-8): ").strip()
        
        if choice == '0':
            # 功能：程式結束
            print("感謝使用計算機，再見！")
            break
            
        elif choice == '5':
            # 功能：查看運算歷史
            history = calc.get_history()
            if history:
                print("\n運算歷史：")
                for i, record in enumerate(history, 1):
                    print(f"{i}. {record}")
            else:
                print("尚無運算記錄")
                
        elif choice == '6':
            # 功能：清除運算歷史
            calc.clear_history()
            print("運算歷史已清除")
        elif choice == '7':
            # 功能：數值微分計算
            try:
                # 步驟 1: 取得函數表達式
                print("\n請輸入函數表達式，變數名稱為 x，例如: x**2 + 3*x + 1 或 sin(x)")
                expr = input("f(x) = ").strip()
                if not expr:
                    print("表達式不可為空！")
                    continue

                # 步驟 2: 取得評估點
                x = get_number("請輸入評估點 x: ")

                # 步驟 3: 選擇數值方法
                method_input = input("選擇數值方法 [1] 五點中央(預設)  [2] 中央差分: ").strip()
                method = 'five_point' if method_input in ['', '1'] else 'central'

                # 步驟 4: 設定步長（可選）
                h_input = input("步長 h (預設 1e-5，直接 Enter 採預設): ").strip()
                h = 1e-5 if h_input == '' else float(h_input)

                # 步驟 5: 建立函數並計算微分
                f = build_function_from_expr(expr)
                result = calc.derivative(f, x, h=h, method=method, label=expr)
                print(f"\n結果: f'(x) 在 x={x} 的近似值為 {result}")
                
            except ValueError as e:
                print(f"錯誤: {e}")
            except Exception as e:
                print(f"錯誤: 無法解析或計算該表達式 ({e})")
        elif choice == '8':
            # 功能：數值積分計算
            try:
                # 步驟 1: 取得函數表達式
                print("\n請輸入函數表達式，變數名稱為 x，例如: x**2 + 3*x + 1 或 sin(x)")
                expr = input("f(x) = ").strip()
                if not expr:
                    print("表達式不可為空！")
                    continue

                # 步驟 2: 取得積分區間
                a = get_number("請輸入積分下限 a: ")
                b = get_number("請輸入積分上限 b: ")
                
                # 驗證積分區間有效性
                if a >= b:
                    print("錯誤: 積分上限必須大於下限！")
                    continue

                # 步驟 3: 選擇數值方法
                method_input = input("選擇數值方法 [1] Simpson法則(預設)  [2] 梯形法則: ").strip()
                method = 'simpson' if method_input in ['', '1'] else 'trapezoidal'

                # 步驟 4: 設定分割數量（可選）
                n_input = input("分割數量 n (預設 1000，直接 Enter 採預設): ").strip()
                n = 1000 if n_input == '' else int(n_input)
                if n <= 0:
                    print("分割數量必須為正整數！")
                    continue

                # 步驟 5: 建立函數並計算積分
                f = build_function_from_expr(expr)
                result = calc.integrate(f, a, b, n=n, method=method, label=expr)
                print(f"\n結果: ∫ f(x) dx 從 {a} 到 {b} 的近似值為 {result}")
                
            except ValueError as e:
                print(f"錯誤: {e}")
            except Exception as e:
                print(f"錯誤: 無法解析或計算該表達式 ({e})")
        elif choice in ['1', '2', '3', '4']:
            # 功能：基本四則運算
            try:
                # 步驟 1: 確認運算類型（雖然已經選擇，但再次確認運算符號）
                operation = get_operation()
                if operation:
                    # 步驟 2: 取得運算數
                    a = get_number("請輸入第一個數字: ")
                    b = get_number("請輸入第二個數字: ")
                    
                    # 步驟 3: 執行運算並顯示結果
                    result = calc.calculate(operation, a, b)
                    print(f"\n結果: {result}")
                    
            except ValueError as e:
                print(f"錯誤: {e}")
                
        else:
            # 處理無效選擇
            print("無效的選擇，請重新輸入！")
        
        # 等待使用者確認後繼續
        input("\n按 Enter 鍵繼續...")

if __name__ == "__main__":
    """
    程式入口點
    
    當檔案被直接執行時（而非被匯入時），執行主程式。
    包含最頂層的異常處理，捕捉使用者中斷（Ctrl+C）。
    """
    try:
        # 執行主程式
        main()
    except KeyboardInterrupt:
        # 處理使用者中斷（Ctrl+C）
        print("\n\n程式被中斷，再見！")
        sys.exit(0)
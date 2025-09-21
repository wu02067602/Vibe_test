#!/usr/bin/env python3
"""
計算機主程式
提供命令列介面讓使用者進行計算
"""

import sys
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

def main():
    """主程式"""
    calc = Calculator()
    
    print("歡迎使用計算機！")
    
    while True:
        display_menu()
        choice = input("請選擇功能 (0-6): ").strip()
        
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
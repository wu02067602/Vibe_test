#!/usr/bin/env python3
"""
愛心圖案生成器
使用數學方程式繪製愛心形狀
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # 使用非互動式後端
import matplotlib.pyplot as plt


def draw_heart():
    """繪製愛心圖案"""
    # 使用參數方程式繪製心形
    # x = 16sin³(t)
    # y = 13cos(t) - 5cos(2t) - 2cos(3t) - cos(4t)
    
    t = np.linspace(0, 2 * np.pi, 1000)
    
    x = 16 * np.sin(t)**3
    y = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)
    
    # 創建圖形
    plt.figure(figsize=(10, 10))
    plt.plot(x, y, color='red', linewidth=3)
    plt.fill(x, y, color='red', alpha=0.7)
    
    # 設置圖形樣式
    plt.title('❤️ 愛心 ❤️', fontsize=24, fontweight='bold')
    plt.axis('equal')
    plt.grid(True, alpha=0.3)
    plt.xlabel('x', fontsize=14)
    plt.ylabel('y', fontsize=14)
    
    # 添加背景色
    plt.gca().set_facecolor('#ffe6f0')
    plt.gcf().patch.set_facecolor('white')
    
    # 保存圖形
    plt.tight_layout()
    plt.savefig('heart.png', dpi=300, bbox_inches='tight')
    print("✨ 愛心已生成並保存為 heart.png")
    print("📁 圖片檔案: heart.png")
    plt.close()


def print_ascii_heart():
    """在終端機打印 ASCII 愛心"""
    heart = """
    ❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️
    
        ♥♥♥♥♥♥    ♥♥♥♥♥♥
      ♥♥♥♥♥♥♥♥♥♥  ♥♥♥♥♥♥♥♥♥♥
     ♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥
     ♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥
     ♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥
      ♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥
       ♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥
         ♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥
          ♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥
            ♥♥♥♥♥♥♥♥♥♥♥
              ♥♥♥♥♥♥♥
                ♥♥♥
                 ♥
    
    ❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️
    """
    print(heart)


if __name__ == "__main__":
    print("=" * 50)
    print("           🌹 愛心生成器 🌹")
    print("=" * 50)
    
    # 先顯示 ASCII 愛心
    print_ascii_heart()
    
    # 詢問是否繪製圖形愛心
    choice = input("\n是否要繪製圖形愛心？(y/n): ").strip().lower()
    
    if choice == 'y' or choice == 'yes' or choice == '':
        try:
            draw_heart()
        except ImportError:
            print("⚠️  需要安裝 matplotlib 和 numpy 套件")
            print("請執行: pip install matplotlib numpy")
    else:
        print("👋 再見！")

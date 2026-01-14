"""
Python 環境診斷腳本
"""

import sys
import subprocess

print("=" * 70)
print("Python 環境診斷")
print("=" * 70)

# 1. 檢查 Python 路徑
print(f"\n1. Python 執行檔路徑:")
print(f"   {sys.executable}")

# 2. 檢查 Python 版本
print(f"\n2. Python 版本:")
print(f"   {sys.version}")

# 3. 檢查 site-packages 路徑
print(f"\n3. 模組搜尋路徑:")
for i, path in enumerate(sys.path[:5], 1):
    print(f"   {i}. {path}")

# 4. 嘗試導入 streamlit
print(f"\n4. 測試導入 streamlit:")
try:
    import streamlit
    print(f"   ✓ 成功導入 streamlit")
    print(f"   版本: {streamlit.__version__}")
    print(f"   位置: {streamlit.__file__}")
except ImportError as e:
    print(f"   ✗ 無法導入 streamlit")
    print(f"   錯誤: {e}")

# 5. 檢查已安裝的套件
print(f"\n5. 檢查已安裝的關鍵套件:")
packages = ['streamlit', 'pandas', 'numpy', 'yfinance', 'twstock', 'plotly']

for pkg in packages:
    try:
        module = __import__(pkg)
        version = getattr(module, '__version__', 'unknown')
        print(f"   ✓ {pkg:15} - {version}")
    except ImportError:
        print(f"   ✗ {pkg:15} - 未安裝")

# 6. 顯示 pip 資訊
print(f"\n6. pip 安裝位置:")
result = subprocess.run([sys.executable, '-m', 'pip', '--version'],
                       capture_output=True, text=True)
print(f"   {result.stdout.strip()}")

print("\n" + "=" * 70)
print("診斷完成")
print("=" * 70)

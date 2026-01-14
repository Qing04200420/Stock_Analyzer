"""
測試修復後的資料獲取功能
"""

import sys
sys.path.append('.')

from backend.modules.data_fetcher import TaiwanStockDataFetcher

print("=" * 60)
print("測試修復後的資料獲取功能")
print("=" * 60)

fetcher = TaiwanStockDataFetcher()

print("\n1. 測試獲取台積電 (2330) 資料...")
df = fetcher.get_stock_price('2330', days=30)

if not df.empty:
    print(f"✓ 成功獲取資料")
    print(f"  資料筆數: {len(df)}")
    print(f"  欄位: {list(df.columns)}")
    print(f"\n最近5天資料:")
    print(df.tail())
    print(f"\n最新收盤價: {df['收盤價'].iloc[-1]:.2f}")
else:
    print("✗ 無法獲取資料")

print("\n" + "=" * 60)
print("測試完成")
print("=" * 60)

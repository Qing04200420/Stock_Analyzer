"""
測試真實資料獲取
"""

import sys
sys.path.append('.')

from backend.modules.data_fetcher import TaiwanStockDataFetcher

print("=" * 60)
print("Testing Real Data Fetch")
print("=" * 60)

fetcher = TaiwanStockDataFetcher()

print("\n1. Fetching TSMC (2330) data...")
df = fetcher.get_stock_price('2330', days=5)

if not df.empty:
    print("SUCCESS - Data retrieved!")
    print(f"  Rows: {len(df)}")
    print(f"  Columns: {list(df.columns)}")
    print(f"\nLatest data:")
    print(df.tail())
    latest_price = df['收盤價'].iloc[-1]
    print(f"\nLatest closing price: {latest_price:.2f}")

    # 驗證價格是否合理（台積電應該在 400-800 之間）
    if 400 <= latest_price <= 900:
        print("PASS - Price looks reasonable for TSMC")
    else:
        print(f"WARNING - Price {latest_price} seems unusual for TSMC")
else:
    print("FAILED - No data retrieved")

print("\n" + "=" * 60)

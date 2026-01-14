# -*- coding: utf-8 -*-
"""
測試原始 FinMind API 返回的資料
"""

from FinMind.data import DataLoader
from datetime import datetime, timedelta

print("=" * 70)
print("測試原始 FinMind API")
print("=" * 70)

dl = DataLoader()

# Calculate date range
end_date = datetime.now().strftime("%Y-%m-%d")
start_date = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")

print(f"\nFetching data for 2330 from {start_date} to {end_date}...")

# Get raw data
df = dl.taiwan_stock_daily(
    stock_id="2330",
    start_date=start_date,
    end_date=end_date
)

print(f"\nDataFrame type: {type(df)}")
print(f"DataFrame shape: {df.shape}")
print(f"DataFrame columns: {df.columns.tolist()}")
print(f"\nDataFrame dtypes:")
print(df.dtypes)
print(f"\nFirst 3 rows:")
print(df.head(3))
print(f"\nLast 3 rows:")
print(df.tail(3))

# Check specific values
if not df.empty:
    print(f"\nLast row details:")
    last_row = df.iloc[-1]
    print(f"  date: {last_row['date']}")
    print(f"  stock_id: {last_row['stock_id']}")
    print(f"  open: {last_row['open']} (type: {type(last_row['open'])})")
    print(f"  close: {last_row['close']} (type: {type(last_row['close'])})")
    print(f"  max: {last_row['max']} (type: {type(last_row['max'])})")
    print(f"  min: {last_row['min']} (type: {type(last_row['min'])})")
    print(f"  Trading_Volume: {last_row['Trading_Volume']} (type: {type(last_row['Trading_Volume'])})")

print("\n" + "=" * 70)

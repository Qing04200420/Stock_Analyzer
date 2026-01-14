# -*- coding: utf-8 -*-
"""
測試 FinMind 資料是否正確
檢查資料值而非顯示問題
"""

import sys
import pandas as pd
from backend.modules.finmind_fetcher import FinMindDataFetcher
from backend.modules.data_fetcher_ultimate import UltimateTaiwanStockDataFetcher

def test_finmind_direct():
    """直接測試 FinMind"""
    print("\n" + "=" * 70)
    print("測試 1: FinMind 直接獲取")
    print("=" * 70)

    fetcher = FinMindDataFetcher()
    df = fetcher.get_stock_price("2330", days=5)

    print(f"\nDataFrame shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    print(f"Index: {df.index.tolist()}")
    print(f"\nFirst row data:")

    if not df.empty:
        first_row = df.iloc[0]
        print(f"  Index: {df.index[0]}")
        for col in df.columns:
            print(f"  {repr(col)}: {first_row[col]}")

        # Check if values are valid numbers
        last_row = df.iloc[-1]
        print(f"\nLast row data:")
        print(f"  Index: {df.index[-1]}")
        for col in df.columns:
            val = last_row[col]
            print(f"  {repr(col)}: {val} (type: {type(val).__name__}, isnan: {pd.isna(val)})")

    return df


def test_ultimate_fetcher():
    """測試終極版獲取器"""
    print("\n" + "=" * 70)
    print("測試 2: 終極版獲取器")
    print("=" * 70)

    fetcher = UltimateTaiwanStockDataFetcher()
    df = fetcher.get_stock_price("2330", days=5)

    print(f"\nDataFrame shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    print(f"Index: {df.index.tolist()}")
    print(f"\nFirst row data:")

    if not df.empty:
        first_row = df.iloc[0]
        print(f"  Index: {df.index[0]}")
        for col in df.columns:
            print(f"  {repr(col)}: {first_row[col]}")

        # Check if values are valid numbers
        last_row = df.iloc[-1]
        print(f"\nLast row data:")
        print(f"  Index: {df.index[-1]}")
        for col in df.columns:
            val = last_row[col]
            print(f"  {repr(col)}: {val} (type: {type(val).__name__}, isnan: {pd.isna(val)})")

        # Show stats
        print(f"\nStats: {fetcher.get_stats()}")

    return df


def compare_data(df1, df2):
    """比較兩個 DataFrame"""
    print("\n" + "=" * 70)
    print("比較結果")
    print("=" * 70)

    print(f"\nFinMind columns: {df1.columns.tolist()}")
    print(f"Ultimate columns: {df2.columns.tolist()}")

    # Check if columns match (ignoring encoding display issues)
    print(f"\nNumber of columns match: {len(df1.columns) == len(df2.columns)}")
    print(f"Number of rows match: {len(df1) == len(df2)}")

    if not df1.empty and not df2.empty:
        # Compare last row values
        print(f"\nLast row comparison:")
        print(f"  FinMind last close: {df1.iloc[-1].iloc[3] if len(df1.columns) > 3 else 'N/A'}")
        print(f"  Ultimate last close: {df2.iloc[-1].iloc[3] if len(df2.columns) > 3 else 'N/A'}")


if __name__ == "__main__":
    print("=" * 70)
    print("FinMind 資料診斷測試")
    print("=" * 70)

    df1 = test_finmind_direct()
    df2 = test_ultimate_fetcher()
    compare_data(df1, df2)

    print("\n" + "=" * 70)
    print("測試完成")
    print("=" * 70)
